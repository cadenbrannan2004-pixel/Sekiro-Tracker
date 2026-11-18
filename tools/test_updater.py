import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path
from unittest import mock

from sekiro_tracker import updater

NEW_EXE = b"new build"


def fake_urlopen(release):
    def urlopen(url, timeout):
        return io.BytesIO(json.dumps(release).encode() if url == updater.LATEST_RELEASE else NEW_EXE)
    return urlopen


def release(tag, digest="sha256:" + hashlib.sha256(NEW_EXE).hexdigest()):
    return {"tag_name": tag, "assets": [{"name": updater.ASSET_NAME, "browser_download_url": "x", "digest": digest}]}


def main():
    with mock.patch.object(updater, "FROZEN", True), mock.patch.object(updater, "VERSION", "1.1.0"):
        for tag, newer in [("v1.1.0", False), ("v1.0.9", False), ("v1.10.0", True), ("v2.0-beta", False)]:
            with mock.patch("urllib.request.urlopen", fake_urlopen(release(tag))):
                assert (updater.check() is not None) == newer, tag
        with mock.patch("urllib.request.urlopen", fake_urlopen(release("v9.0.0", digest=None))):
            assert updater.check() is None, "missing checksum must mean no update"

        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / updater.ASSET_NAME
            with mock.patch.object(sys, "executable", str(exe)), mock.patch("subprocess.Popen") as popen, \
                 mock.patch("urllib.request.urlopen", fake_urlopen(release("v9.0.0"))):
                exe.write_bytes(b"old build")
                try:
                    updater.install({**updater.check(), "sha256": "0" * 64})
                    raise AssertionError("a bad checksum must not install")
                except ValueError:
                    pass
                assert exe.read_bytes() == b"old build" and not exe.with_name(exe.name + ".new").exists()
                popen.assert_not_called()

                updater.install(updater.check())
                assert exe.read_bytes() == NEW_EXE
                assert exe.with_name(exe.name + ".old").read_bytes() == b"old build"
                assert popen.call_args.kwargs["env"]["PYINSTALLER_RESET_ENVIRONMENT"] == "1"

                updater.remove_leftover()
                assert not exe.with_name(exe.name + ".old").exists()
    print("updater ok")


if __name__ == "__main__":
    main()
