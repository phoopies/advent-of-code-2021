print(
    len([e for row in list(
        map(lambda l: list(filter(lambda e: len(e) in [2, 3, 4, 7], l)),
            map(lambda l: l.split(' '),
                map(lambda l: l.split('|')[1],
                [line.strip() for line in open("day8/input")]
                )
            )
       )
    ) for e in row])
)
