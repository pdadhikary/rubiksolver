import pytest

from rubiksolver.cube import (
    CubeFace,
    CubeLabel,
    CubePositon,
    Facelet,
    RubiksCube,
)


@pytest.fixture
def cube() -> RubiksCube:
    return RubiksCube()


@pytest.fixture
def cube_initalized() -> RubiksCube:
    obj = RubiksCube()

    for face in CubeFace:
        for position in CubePositon:
            obj.setFaceletLabel(Facelet(face, position), CubeLabel(face.value))

    return obj


@pytest.mark.parametrize(
    "facelet, expected",
    [
        (Facelet(CubeFace.UP, CubePositon.ONE), 0),
        (Facelet(CubeFace.UP, CubePositon.TWO), 1),
        (Facelet(CubeFace.UP, CubePositon.THREE), 2),
        (Facelet(CubeFace.UP, CubePositon.FOUR), 3),
        (Facelet(CubeFace.UP, CubePositon.FIVE), 4),
        (Facelet(CubeFace.UP, CubePositon.SIX), 5),
        (Facelet(CubeFace.UP, CubePositon.SEVEN), 6),
        (Facelet(CubeFace.UP, CubePositon.EIGHT), 7),
        (Facelet(CubeFace.UP, CubePositon.NINE), 8),
        (Facelet(CubeFace.RIGHT, CubePositon.ONE), 9),
        (Facelet(CubeFace.RIGHT, CubePositon.TWO), 10),
        (Facelet(CubeFace.RIGHT, CubePositon.THREE), 11),
        (Facelet(CubeFace.RIGHT, CubePositon.FOUR), 12),
        (Facelet(CubeFace.RIGHT, CubePositon.FIVE), 13),
        (Facelet(CubeFace.RIGHT, CubePositon.SIX), 14),
        (Facelet(CubeFace.RIGHT, CubePositon.SEVEN), 15),
        (Facelet(CubeFace.RIGHT, CubePositon.EIGHT), 16),
        (Facelet(CubeFace.RIGHT, CubePositon.NINE), 17),
        (Facelet(CubeFace.FRONT, CubePositon.ONE), 18),
        (Facelet(CubeFace.FRONT, CubePositon.TWO), 19),
        (Facelet(CubeFace.FRONT, CubePositon.THREE), 20),
        (Facelet(CubeFace.FRONT, CubePositon.FOUR), 21),
        (Facelet(CubeFace.FRONT, CubePositon.FIVE), 22),
        (Facelet(CubeFace.FRONT, CubePositon.SIX), 23),
        (Facelet(CubeFace.FRONT, CubePositon.SEVEN), 24),
        (Facelet(CubeFace.FRONT, CubePositon.EIGHT), 25),
        (Facelet(CubeFace.FRONT, CubePositon.NINE), 26),
        (Facelet(CubeFace.DOWN, CubePositon.ONE), 27),
        (Facelet(CubeFace.DOWN, CubePositon.TWO), 28),
        (Facelet(CubeFace.DOWN, CubePositon.THREE), 29),
        (Facelet(CubeFace.DOWN, CubePositon.FOUR), 30),
        (Facelet(CubeFace.DOWN, CubePositon.FIVE), 31),
        (Facelet(CubeFace.DOWN, CubePositon.SIX), 32),
        (Facelet(CubeFace.DOWN, CubePositon.SEVEN), 33),
        (Facelet(CubeFace.DOWN, CubePositon.EIGHT), 34),
        (Facelet(CubeFace.DOWN, CubePositon.NINE), 35),
        (Facelet(CubeFace.LEFT, CubePositon.ONE), 36),
        (Facelet(CubeFace.LEFT, CubePositon.TWO), 37),
        (Facelet(CubeFace.LEFT, CubePositon.THREE), 38),
        (Facelet(CubeFace.LEFT, CubePositon.FOUR), 39),
        (Facelet(CubeFace.LEFT, CubePositon.FIVE), 40),
        (Facelet(CubeFace.LEFT, CubePositon.SIX), 41),
        (Facelet(CubeFace.LEFT, CubePositon.SEVEN), 42),
        (Facelet(CubeFace.LEFT, CubePositon.EIGHT), 43),
        (Facelet(CubeFace.LEFT, CubePositon.NINE), 44),
        (Facelet(CubeFace.BACK, CubePositon.ONE), 45),
        (Facelet(CubeFace.BACK, CubePositon.TWO), 46),
        (Facelet(CubeFace.BACK, CubePositon.THREE), 47),
        (Facelet(CubeFace.BACK, CubePositon.FOUR), 48),
        (Facelet(CubeFace.BACK, CubePositon.FIVE), 49),
        (Facelet(CubeFace.BACK, CubePositon.SIX), 50),
        (Facelet(CubeFace.BACK, CubePositon.SEVEN), 51),
        (Facelet(CubeFace.BACK, CubePositon.EIGHT), 52),
        (Facelet(CubeFace.BACK, CubePositon.NINE), 53),
    ],
)
def test_FaceletToIndex(facelet, expected):
    assert RubiksCube.FaceletToIndex(facelet) == expected


def test_str(cube: RubiksCube):
    assert str(cube) == (
        "XXXXUXXXX" "XXXXRXXXX" "XXXXFXXXX" "XXXXDXXXX" "XXXXLXXXX" "XXXXBXXXX"
    )


@pytest.mark.parametrize(
    "facelet1, facelet2, expected",
    [
        (
            Facelet(CubeFace.UP, CubePositon.FIVE),
            Facelet(CubeFace.RIGHT, CubePositon.FIVE),
            "XXXXRXXXX"
            "XXXXUXXXX"
            "XXXXFXXXX"
            "XXXXDXXXX"
            "XXXXLXXXX"
            "XXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePositon.FIVE),
            Facelet(CubeFace.FRONT, CubePositon.FIVE),
            "XXXXFXXXX"
            "XXXXRXXXX"
            "XXXXUXXXX"
            "XXXXDXXXX"
            "XXXXLXXXX"
            "XXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePositon.FIVE),
            Facelet(CubeFace.DOWN, CubePositon.FIVE),
            "XXXXDXXXX"
            "XXXXRXXXX"
            "XXXXFXXXX"
            "XXXXUXXXX"
            "XXXXLXXXX"
            "XXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePositon.FIVE),
            Facelet(CubeFace.LEFT, CubePositon.FIVE),
            "XXXXLXXXX"
            "XXXXRXXXX"
            "XXXXFXXXX"
            "XXXXDXXXX"
            "XXXXUXXXX"
            "XXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePositon.FIVE),
            Facelet(CubeFace.BACK, CubePositon.FIVE),
            "XXXXBXXXX"
            "XXXXRXXXX"
            "XXXXFXXXX"
            "XXXXDXXXX"
            "XXXXLXXXX"
            "XXXXUXXXX",
        ),
    ],
)
def test_swapFacelets(
    cube: RubiksCube, facelet1: Facelet, facelet2: Facelet, expected: str
):
    cube._swapFacelets(facelet1, facelet2)
    assert str(cube) == expected


@pytest.mark.parametrize(
    "moves, expected",
    [
        (
            ["rotateUpCW"],
            "UUUUUUUUU"
            "BBBRRRRRR"
            "RRRFFFFFF"
            "DDDDDDDDD"
            "FFFLLLLLL"
            "LLLBBBBBB",
        ),
        (
            ["rotateUpCCW"],
            "UUUUUUUUU"
            "FFFRRRRRR"
            "LLLFFFFFF"
            "DDDDDDDDD"
            "BBBLLLLLL"
            "RRRBBBBBB",
        ),
        (
            ["rotateUpCW", "rotateUpCCW"],
            "UUUUUUUUU"
            "RRRRRRRRR"
            "FFFFFFFFF"
            "DDDDDDDDD"
            "LLLLLLLLL"
            "BBBBBBBBB",
        ),
        (
            ["rotateRightCW"],
            "UUFUUFUUF"
            "RRRRRRRRR"
            "FFDFFDFFD"
            "DDBDDBDDB"
            "LLLLLLLLL"
            "UBBUBBUBB",
        ),
        (
            ["rotateRightCCW"],
            "UUBUUBUUB"
            "RRRRRRRRR"
            "FFUFFUFFU"
            "DDFDDFDDF"
            "LLLLLLLLL"
            "DBBDBBDBB",
        ),
        (
            ["rotateRightCW", "rotateRightCCW"],
            "UUUUUUUUU"
            "RRRRRRRRR"
            "FFFFFFFFF"
            "DDDDDDDDD"
            "LLLLLLLLL"
            "BBBBBBBBB",
        ),
        (
            ["rotateFrontCW"],
            "UUUUUULLL"
            "URRURRURR"
            "FFFFFFFFF"
            "RRRDDDDDD"
            "LLDLLDLLD"
            "BBBBBBBBB",
        ),
        (
            ["rotateFrontCCW"],
            "UUUUUURRR"
            "DRRDRRDRR"
            "FFFFFFFFF"
            "LLLDDDDDD"
            "LLULLULLU"
            "BBBBBBBBB",
        ),
        (
            ["rotateFrontCW", "rotateFrontCCW"],
            "UUUUUUUUU"
            "RRRRRRRRR"
            "FFFFFFFFF"
            "DDDDDDDDD"
            "LLLLLLLLL"
            "BBBBBBBBB",
        ),
        (
            ["rotateDownCW"],
            "UUUUUUUUU"
            "RRRRRRFFF"
            "FFFFFFLLL"
            "DDDDDDDDD"
            "LLLLLLBBB"
            "BBBBBBRRR",
        ),
        (
            ["rotateDownCCW"],
            "UUUUUUUUU"
            "RRRRRRBBB"
            "FFFFFFRRR"
            "DDDDDDDDD"
            "LLLLLLFFF"
            "BBBBBBLLL",
        ),
        (
            ["rotateDownCW", "rotateDownCCW"],
            "UUUUUUUUU"
            "RRRRRRRRR"
            "FFFFFFFFF"
            "DDDDDDDDD"
            "LLLLLLLLL"
            "BBBBBBBBB",
        ),
        (
            ["rotateLeftCW"],
            "BUUBUUBUU"
            "RRRRRRRRR"
            "UFFUFFUFF"
            "FDDFDDFDD"
            "LLLLLLLLL"
            "BBDBBDBBD",
        ),
        (
            ["rotateLeftCCW"],
            "FUUFUUFUU"
            "RRRRRRRRR"
            "DFFDFFDFF"
            "BDDBDDBDD"
            "LLLLLLLLL"
            "BBUBBUBBU",
        ),
        (
            ["rotateLeftCW", "rotateLeftCCW"],
            "UUUUUUUUU"
            "RRRRRRRRR"
            "FFFFFFFFF"
            "DDDDDDDDD"
            "LLLLLLLLL"
            "BBBBBBBBB",
        ),
        (
            ["rotateBackCW"],
            "RRRUUUUUU"
            "RRDRRDRRD"
            "FFFFFFFFF"
            "DDDDDDLLL"
            "ULLULLULL"
            "BBBBBBBBB",
        ),
        (
            ["rotateBackCCW"],
            "LLLUUUUUU"
            "RRURRURRU"
            "FFFFFFFFF"
            "DDDDDDRRR"
            "DLLDLLDLL"
            "BBBBBBBBB",
        ),
        (
            ["rotateBackCW", "rotateBackCCW"],
            "UUUUUUUUU"
            "RRRRRRRRR"
            "FFFFFFFFF"
            "DDDDDDDDD"
            "LLLLLLLLL"
            "BBBBBBBBB",
        ),
        (
            ["rotateRightCW", "rotateUpCW", "rotateRightCCW", "rotateUpCCW"],
            "UULUUFUUF"
            "RRUBRRURR"
            "FFDFFUFFF"
            "DDRDDDDDD"
            "BLLLLLLLL"
            "BRRBBBBBB",
        ),
        (
            ["rotateRightCW", "rotateUpCW", "rotateRightCCW", "rotateUpCCW"]
            * 6,
            "UUUUUUUUU"
            "RRRRRRRRR"
            "FFFFFFFFF"
            "DDDDDDDDD"
            "LLLLLLLLL"
            "BBBBBBBBB",
        ),
        (
            [
                "rotateUpCW",
                "rotateUpCW",
                "rotateFrontCCW",
                "rotateRightCW",
                "rotateBackCW",
                "rotateBackCW",
                "rotateRightCW",
                "rotateRightCW",
                "rotateDownCW",
                "rotateRightCW",
                "rotateRightCW",
                "rotateDownCW",
                "rotateDownCW",
                "rotateFrontCW",
                "rotateFrontCW",
                "rotateDownCCW",
                "rotateRightCCW",
                "rotateDownCCW",
                "rotateBackCW",
                "rotateBackCW",
                "rotateRightCW",
                "rotateRightCW",
                "rotateUpCCW",
                "rotateBackCW",
                "rotateBackCW",
                "rotateUpCW",
                "rotateRightCW",
                "rotateRightCW",
                "rotateDownCW",
                "rotateDownCW",
                "rotateFrontCW",
                "rotateFrontCW",
                "rotateDownCCW",
            ],
            "DRLUUBFBR"
            "BLURRLRUB"
            "LRDDFDLFU"
            "FUFFDBRDU"
            "BRUFLLFDD"
            "BFLUBLRBD",
        ),
    ],
)
def test_moves(cube_initalized: RubiksCube, moves: list[str], expected: str):
    for move in moves:
        move_func = getattr(cube_initalized, move)
        move_func()

    assert str(cube_initalized) == expected


@pytest.mark.parametrize(
    "moves",
    [
        [
            "rotateUpCW",
            "rotateUpCW",
            "rotateFrontCCW",
            "rotateRightCW",
            "rotateBackCW",
            "rotateBackCW",
            "rotateRightCW",
            "rotateRightCW",
            "rotateDownCW",
            "rotateRightCW",
            "rotateRightCW",
            "rotateDownCW",
            "rotateDownCW",
            "rotateFrontCW",
            "rotateFrontCW",
            "rotateDownCCW",
            "rotateRightCCW",
            "rotateDownCCW",
            "rotateBackCW",
            "rotateBackCW",
            "rotateRightCW",
            "rotateRightCW",
            "rotateUpCCW",
            "rotateBackCW",
            "rotateBackCW",
            "rotateUpCW",
            "rotateRightCW",
            "rotateRightCW",
            "rotateDownCW",
            "rotateDownCW",
            "rotateFrontCW",
            "rotateFrontCW",
            "rotateDownCCW",
        ]
    ],
)
def test_getFaceletLabel(cube_initalized: RubiksCube, moves: list[str]):
    for move in moves:
        move_func = getattr(cube_initalized, move)
        move_func()

    current_state: list[CubeLabel] = []
    for face in CubeFace:
        for position in CubePositon:
            current_state.append(
                cube_initalized.getFaceletLabel(Facelet(face, position))
            )

    assert current_state == cube_initalized.state
