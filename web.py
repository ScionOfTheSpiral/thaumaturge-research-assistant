from pathlib import Path

import streamlit as st

from aspect_engine import AspectLibrary
from thaum_elements import ASPECTS

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ICON_WIDTH = 40
PATH_ROW_SIZE = 6  # icons per row in the result, so long paths wrap


def icon_path(aspect: str) -> Path:
    """Aspect PNGs"""
    return ASSETS_DIR / f"{aspect}.png"


def show_aspect(container, aspect: str):
    """Draw an aspect's icon with its name, falling back to text only."""
    path = icon_path(aspect)
    if path.exists():
        container.image(str(path), width=ICON_WIDTH)
    container.caption(aspect)


@st.cache_resource
def load_library():
    return AspectLibrary(ASPECTS)


lib = load_library()
aspects = sorted(lib.all_aspects())

st.title("Thaumcraft Aspect Solver")

col1, col2 = st.columns(2)
start = col1.selectbox("Start", aspects)
show_aspect(col1, start)  # selectboxes can't hold icons, so preview below
target = col2.selectbox("Target", aspects, index=1)
show_aspect(col2, target)

spaces = st.number_input("Spaces between", min_value=0, value=3)

if st.button("Find path"):
    path = lib.pathfinding(start, target, min_spaces=spaces)
    if path:
        st.success(" \u2192 ".join(path))
        for i in range(0, len(path), PATH_ROW_SIZE):
            row = path[i : i + PATH_ROW_SIZE]
            cols = st.columns(PATH_ROW_SIZE)  # fixed width keeps rows aligned
            for col, aspect in zip(cols, row):
                show_aspect(col, aspect)
    else:
        st.error("No path found.")