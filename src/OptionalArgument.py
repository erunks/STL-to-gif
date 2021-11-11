class OptionalArgument:
    def __init__(self, name, args):
        self.raw_args = args
        self.name = name
        self.long = args["long"]
        self.default = args["default"]
        self.description = args["description"]

        if "short" in args:
            self.short = args["short"]
        else:
            self.short = ""

        if "value" in args:
            self.value = args["value"]
        else:
            self.value = self.default

    def get_value(self):
        return self.value
