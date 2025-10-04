import pytest

from rubiksolver.cube import CubeFace, CubeLabel, CubePosition, Facelet, RubiksCube


@pytest.fixture
def cube() -> RubiksCube:
    return RubiksCube()


@pytest.fixture
def cube_initalized() -> RubiksCube:
    obj = RubiksCube()

    for face in CubeFace:
        for position in CubePosition:
            obj.setFaceletLabel(Facelet(face, position), CubeLabel(face.value))

    return obj


@pytest.mark.parametrize(
    "facelet, expected",
    [
        (Facelet(CubeFace.UP, CubePosition.ONE), 0),
        (Facelet(CubeFace.UP, CubePosition.TWO), 1),
        (Facelet(CubeFace.UP, CubePosition.THREE), 2),
        (Facelet(CubeFace.UP, CubePosition.FOUR), 3),
        (Facelet(CubeFace.UP, CubePosition.FIVE), 4),
        (Facelet(CubeFace.UP, CubePosition.SIX), 5),
        (Facelet(CubeFace.UP, CubePosition.SEVEN), 6),
        (Facelet(CubeFace.UP, CubePosition.EIGHT), 7),
        (Facelet(CubeFace.UP, CubePosition.NINE), 8),
        (Facelet(CubeFace.RIGHT, CubePosition.ONE), 9),
        (Facelet(CubeFace.RIGHT, CubePosition.TWO), 10),
        (Facelet(CubeFace.RIGHT, CubePosition.THREE), 11),
        (Facelet(CubeFace.RIGHT, CubePosition.FOUR), 12),
        (Facelet(CubeFace.RIGHT, CubePosition.FIVE), 13),
        (Facelet(CubeFace.RIGHT, CubePosition.SIX), 14),
        (Facelet(CubeFace.RIGHT, CubePosition.SEVEN), 15),
        (Facelet(CubeFace.RIGHT, CubePosition.EIGHT), 16),
        (Facelet(CubeFace.RIGHT, CubePosition.NINE), 17),
        (Facelet(CubeFace.FRONT, CubePosition.ONE), 18),
        (Facelet(CubeFace.FRONT, CubePosition.TWO), 19),
        (Facelet(CubeFace.FRONT, CubePosition.THREE), 20),
        (Facelet(CubeFace.FRONT, CubePosition.FOUR), 21),
        (Facelet(CubeFace.FRONT, CubePosition.FIVE), 22),
        (Facelet(CubeFace.FRONT, CubePosition.SIX), 23),
        (Facelet(CubeFace.FRONT, CubePosition.SEVEN), 24),
        (Facelet(CubeFace.FRONT, CubePosition.EIGHT), 25),
        (Facelet(CubeFace.FRONT, CubePosition.NINE), 26),
        (Facelet(CubeFace.DOWN, CubePosition.ONE), 27),
        (Facelet(CubeFace.DOWN, CubePosition.TWO), 28),
        (Facelet(CubeFace.DOWN, CubePosition.THREE), 29),
        (Facelet(CubeFace.DOWN, CubePosition.FOUR), 30),
        (Facelet(CubeFace.DOWN, CubePosition.FIVE), 31),
        (Facelet(CubeFace.DOWN, CubePosition.SIX), 32),
        (Facelet(CubeFace.DOWN, CubePosition.SEVEN), 33),
        (Facelet(CubeFace.DOWN, CubePosition.EIGHT), 34),
        (Facelet(CubeFace.DOWN, CubePosition.NINE), 35),
        (Facelet(CubeFace.LEFT, CubePosition.ONE), 36),
        (Facelet(CubeFace.LEFT, CubePosition.TWO), 37),
        (Facelet(CubeFace.LEFT, CubePosition.THREE), 38),
        (Facelet(CubeFace.LEFT, CubePosition.FOUR), 39),
        (Facelet(CubeFace.LEFT, CubePosition.FIVE), 40),
        (Facelet(CubeFace.LEFT, CubePosition.SIX), 41),
        (Facelet(CubeFace.LEFT, CubePosition.SEVEN), 42),
        (Facelet(CubeFace.LEFT, CubePosition.EIGHT), 43),
        (Facelet(CubeFace.LEFT, CubePosition.NINE), 44),
        (Facelet(CubeFace.BACK, CubePosition.ONE), 45),
        (Facelet(CubeFace.BACK, CubePosition.TWO), 46),
        (Facelet(CubeFace.BACK, CubePosition.THREE), 47),
        (Facelet(CubeFace.BACK, CubePosition.FOUR), 48),
        (Facelet(CubeFace.BACK, CubePosition.FIVE), 49),
        (Facelet(CubeFace.BACK, CubePosition.SIX), 50),
        (Facelet(CubeFace.BACK, CubePosition.SEVEN), 51),
        (Facelet(CubeFace.BACK, CubePosition.EIGHT), 52),
        (Facelet(CubeFace.BACK, CubePosition.NINE), 53),
    ],
)
def test_FaceletToIndex(facelet, expected):
    assert RubiksCube.FaceletToIndex(facelet) == expected


def test_str(cube: RubiksCube):
    assert str(cube) == ("XXXXUXXXXXXXXRXXXXXXXXFXXXXXXXXDXXXXXXXXLXXXXXXXXBXXXX")


@pytest.mark.parametrize(
    "facelet1, facelet2, expected",
    [
        (
            Facelet(CubeFace.UP, CubePosition.FIVE),
            Facelet(CubeFace.RIGHT, CubePosition.FIVE),
            "XXXXRXXXXXXXXUXXXXXXXXFXXXXXXXXDXXXXXXXXLXXXXXXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePosition.FIVE),
            Facelet(CubeFace.FRONT, CubePosition.FIVE),
            "XXXXFXXXXXXXXRXXXXXXXXUXXXXXXXXDXXXXXXXXLXXXXXXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePosition.FIVE),
            Facelet(CubeFace.DOWN, CubePosition.FIVE),
            "XXXXDXXXXXXXXRXXXXXXXXFXXXXXXXXUXXXXXXXXLXXXXXXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePosition.FIVE),
            Facelet(CubeFace.LEFT, CubePosition.FIVE),
            "XXXXLXXXXXXXXRXXXXXXXXFXXXXXXXXDXXXXXXXXUXXXXXXXXBXXXX",
        ),
        (
            Facelet(CubeFace.UP, CubePosition.FIVE),
            Facelet(CubeFace.BACK, CubePosition.FIVE),
            "XXXXBXXXXXXXXRXXXXXXXXFXXXXXXXXDXXXXXXXXLXXXXXXXXUXXXX",
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
            "UUUUUUUUUBBBRRRRRRRRRFFFFFFDDDDDDDDDFFFLLLLLLLLLBBBBBB",
        ),
        (
            ["rotateUpCCW"],
            "UUUUUUUUUFFFRRRRRRLLLFFFFFFDDDDDDDDDBBBLLLLLLRRRBBBBBB",
        ),
        (
            ["rotateUpCW", "rotateUpCCW"],
            "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
        ),
        (
            ["rotateRightCW"],
            "UUFUUFUUFRRRRRRRRRFFDFFDFFDDDBDDBDDBLLLLLLLLLUBBUBBUBB",
        ),
        (
            ["rotateRightCCW"],
            "UUBUUBUUBRRRRRRRRRFFUFFUFFUDDFDDFDDFLLLLLLLLLDBBDBBDBB",
        ),
        (
            ["rotateRightCW", "rotateRightCCW"],
            "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
        ),
        (
            ["rotateFrontCW"],
            "UUUUUULLLURRURRURRFFFFFFFFFRRRDDDDDDLLDLLDLLDBBBBBBBBB",
        ),
        (
            ["rotateFrontCCW"],
            "UUUUUURRRDRRDRRDRRFFFFFFFFFLLLDDDDDDLLULLULLUBBBBBBBBB",
        ),
        (
            ["rotateFrontCW", "rotateFrontCCW"],
            "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
        ),
        (
            ["rotateDownCW"],
            "UUUUUUUUURRRRRRFFFFFFFFFLLLDDDDDDDDDLLLLLLBBBBBBBBBRRR",
        ),
        (
            ["rotateDownCCW"],
            "UUUUUUUUURRRRRRBBBFFFFFFRRRDDDDDDDDDLLLLLLFFFBBBBBBLLL",
        ),
        (
            ["rotateDownCW", "rotateDownCCW"],
            "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
        ),
        (
            ["rotateLeftCW"],
            "BUUBUUBUURRRRRRRRRUFFUFFUFFFDDFDDFDDLLLLLLLLLBBDBBDBBD",
        ),
        (
            ["rotateLeftCCW"],
            "FUUFUUFUURRRRRRRRRDFFDFFDFFBDDBDDBDDLLLLLLLLLBBUBBUBBU",
        ),
        (
            ["rotateLeftCW", "rotateLeftCCW"],
            "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
        ),
        (
            ["rotateBackCW"],
            "RRRUUUUUURRDRRDRRDFFFFFFFFFDDDDDDLLLULLULLULLBBBBBBBBB",
        ),
        (
            ["rotateBackCCW"],
            "LLLUUUUUURRURRURRUFFFFFFFFFDDDDDDRRRDLLDLLDLLBBBBBBBBB",
        ),
        (
            ["rotateBackCW", "rotateBackCCW"],
            "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
        ),
        (
            ["rotateRightCW", "rotateUpCW", "rotateRightCCW", "rotateUpCCW"],
            "UULUUFUUFRRUBRRURRFFDFFUFFFDDRDDDDDDBLLLLLLLLBRRBBBBBB",
        ),
        (
            ["rotateRightCW", "rotateUpCW", "rotateRightCCW", "rotateUpCCW"] * 6,
            "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
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
            "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD",
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
        for position in CubePosition:
            current_state.append(
                cube_initalized.getFaceletLabel(Facelet(face, position))
            )

    assert current_state == cube_initalized.state
