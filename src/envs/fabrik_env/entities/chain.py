from src.envs.core.coordinates import *


class Chain:

    def __init__(self, points: list[Point]) -> None:
        self.links = self._init_links(points)
        total_length = 0.0
        for link in self.links:
            total_length += link.length
        self.total_length = total_length
        self.fingertip_position = self.links[-1].end

    def __repr__(self) -> str:
        message = ''
        for link in self.links:
            message = message + link.__repr__() + '\n'
        return message

    @staticmethod
    def _init_links(points: list[Point]) -> list[Link]:
        links: list[Link] = []

        for i, point in enumerate(points):
            if i == len(points)-1:
                break

            start = point
            end = points[i+1]
            length = np.linalg.norm(end-start)
            angle = np.arctan2(*(reversed(end-start)))

            link = Link(start=start,
                        end=end,
                        length=length,
                        angle=angle)

            links.append(link)

        return links
