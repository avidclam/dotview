from dotview import NA, TreeView, DotView
import dotview


def test_init_exports():
    assert "NA" in dotview.__all__
    assert "TreeView" in dotview.__all__
    assert "DotView" in dotview.__all__
    assert dotview.NA is NA
    assert dotview.TreeView is TreeView
    assert dotview.DotView is DotView
