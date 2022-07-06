import numpy as np

from src.envs.core.coordinates import *
from src.envs.fabrik_env.entities.chain import Chain


class Fabrik:
    TOLERANCE = 0.01

    def iterate(self, chain: Chain, target: Point):
        done = False

        # Check that the end effector can reach the target
        root_point = chain.links[0].start
        distance = np.linalg.norm(target-root_point)
        if distance > chain.total_length:
            return None, False

        # Check if the distance between the end effector and the target is below the tolerance
        end_effector = chain.links[-1].end
        distance = np.linalg.norm(target-end_effector)
        if distance < self.TOLERANCE:
            done = True

        # Backward and forward propagation
        backward_chain = self._backward(chain, target)
        forward_chain = self._forward(backward_chain, chain.links[0].start)
        return forward_chain, done

    
    def _backward(self, chain: Chain, target: Point) -> Chain:
        
        new_points = [target]
        for i, link in enumerate(reversed(chain.links)):
            distance = np.linalg.norm(new_points[i] - link.start)

            relation = link.length/distance

            new_point = (1.0-relation)*new_points[i] + relation*link.start
            new_point = Point(*new_point)

            new_points.append(new_point)

        return Chain(list(reversed(new_points)))

    def _forward(self, chain: Chain, target: Point) -> Chain:
        
        new_points = [target]
        for i, link in enumerate(chain.links):
            distance = np.linalg.norm(link.end - new_points[i])

            relation = link.length/distance

            new_point = (1.0-relation)*new_points[i] + relation*link.end
            new_point = Point(*new_point)

            new_points.append(new_point)

        return Chain(new_points)
        