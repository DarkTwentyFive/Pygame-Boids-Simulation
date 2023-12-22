import pygame
import random
import math

# make boid
class Boid:
    def __init__(self, x, y, width, height):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 2
        self.max_force = 0.03
        self.width = width
        self.height = height

    def update(self, boids):
        separation = self.separate(boids)
        alignment = self.align(boids)
        cohesion = self.cohere(boids)

        separation *= 1.5
        alignment *= 1.0
        cohesion *= 1.0

        self.velocity += separation + alignment + cohesion

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity

        self.position.x = self.position.x % self.width
        self.position.y = self.position.y % self.height

    def seek(self, target):
        desired = (target - self.position).normalize() * self.max_speed
        steer = desired - self.velocity
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer

    def separate(self, boids):
        desired_separation = 25.0
        steer = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if 0 < distance < desired_separation:
                diff = self.position - boid.position
                diff.normalize_ip()
                diff /= distance
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        if steer.length() > 0:
            steer = steer.normalize() * self.max_speed - self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
        return steer

    def align(self, boids):
        neighbordist = 50.0
        sum = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if 0 < distance < neighbordist:
                sum += boid.velocity
                count += 1
        if count > 0:
            sum /= count
            sum.normalize_ip()
            sum *= self.max_speed
            steer = sum - self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer
        else:
            return pygame.Vector2(0, 0)

    def cohere(self, boids):
        neighbordist = 50.0
        sum = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if 0 < distance < neighbordist:
                sum += boid.position
                count += 1
        if count > 0:
            sum /= count
            return self.seek(sum)
        else:
            return pygame.Vector2(0, 0)

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        end_pos = self.position + 10 * pygame.Vector2(math.cos(angle), math.sin(angle))
        pygame.draw.line(screen, (255, 255, 255), self.position, end_pos, 2)

# main boid
def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    boids = [Boid(random.randrange(width), random.randrange(height), width, height) for _ in range(50)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        for boid in boids:
            boid.update(boids)
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
