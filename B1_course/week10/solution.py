class Tee:

    def __init__(self, *destinations):
        self.destinations = destinations

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for destination in self.destinations:
            destination.close()

    def write(self, text):
        for destination in self.destinations:
            destination.write(text)

    def writelines(self, lines):
        for destination in self.destinations:
            destination.writelines(lines)
