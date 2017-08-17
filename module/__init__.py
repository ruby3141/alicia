import importlib
from ..src import router

__all__ = []
pkgs = []

root = router.Router()
for pname in __all__:
	pkg = importlib.import_module("." + pname, __name__)
	pkg.set(root)
	pkgs.append(pkg)

def reload():
	for pkg in pkgs:
		pkg.reload()
		importlib.reload(pkg)
