from sys import maxsize


class Project:
    def __init__(self, id=None, name=None, status=None, enabled=None, inherit_global_categories=True, view_state=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.enabled = enabled
        self.inherit_global_categories = inherit_global_categories
        self.view_state = view_state
        self.description = description

    def __repr__(self):
        return "%s: %s" % (self.id, self.name)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and \
               (self.name is None or other.name is None or self.name == other.name)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize