import dataclasses
import datetime
import sys


@dataclasses.dataclass
class HostNotification:
    ts: datetime.datetime
    notified_user: str
    host: str
    state: str
    notification_command: str
    info: str


def parse_host_notification(ts, rest):
    parts = rest.split(";")
    return HostNotification(ts=ts, notified_user=parts[0], host=parts[1], state=parts[2], notification_command=parts[3], info=parts[4])


@dataclasses.dataclass
class ServiceNotification:
    ts: datetime.datetime
    notified_user: str
    host: str
    service: str
    state: str
    notification_command: str
    info: str


def parse_service_notification(ts, rest):
    parts = rest.split(";")
    return ServiceNotification(ts=ts, notified_user=parts[0], host=parts[1], service=parts[2], state=parts[3], notification_command=parts[4], info=parts[5])


PARSERS_BY_TYPE = {
    "HOST NOTIFICATION": parse_host_notification,
    "SERVICE NOTIFICATION": parse_service_notification,
}


class Parser:
    def parse_log_file(self, f, listener):
        for line in f:
            entry = self.parse_line(line)
            if entry:
                listener(entry)

    def parse_line(self, l):
        split_ts = l.split(" ", 1)
        ts = datetime.datetime.fromtimestamp(int(split_ts[0][1:-1]))
        split_type = split_ts[1].split(":", 1)
        type = split_type[0]
        if type in PARSERS_BY_TYPE:
            return PARSERS_BY_TYPE[type](ts, split_type[1][1:].strip())


def write_notification(entry):
    print("\t".join(map(str, [
        entry.__class__.__name__,
        entry.ts,
        entry.host,
        getattr(entry, "service", ""),
        entry.state,
        entry.info,
    ])))


def extract_notifications():
    with open(sys.argv[1]) as f:
        Parser().parse_log_file(f, write_notification)


if __name__ == "__main__":
    extract_notifications()