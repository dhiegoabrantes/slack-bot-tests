class Event(object):
    def __init__(self, start_datetime, finish_date, initiative, applications, deploy_types):
        self.start_datetime = start_datetime
        self.finish_date = finish_date
        self.initiative = initiative
        self.applications = applications
        self.deploy_types = deploy_types

