#!/usr/bin/env python3

import sys
import os
import argparse
from pathlib import Path

__version__ = "1.0.0"

class Gobble(argparse.Action):
    """
    Gobble grabs the rest of the line and adds it as an array.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        breakpoint()
        dict_object = getattr(namespace, self.dest, None) or {}
        for token in values:
            if "=" in token:
                k, v = token.split("=", 1)
            else:
                k, v = token, True
            dict_object[k.strip()] = v
        setattr(namespace, self.dest, dict_object)


def parse_top_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f",
        "--file",
        help="Specify an alternate compose file",
    )
    parser.add_argument(
        "-p",
        "--project-name",
        help="Specify an alternate project name (default: directory name)",
    )
    parser.add_argument("--profile", help="Specify a profile to enable")
    parser.add_argument("-c", "--context", help="Specify a context name")
    parser.add_argument("--verbose", action="store_true", help="Show more output")
    parser.add_argument(
        "--log-level", help="Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    parser.add_argument(
        "--ansi",
        choices=["never", "always", "auto"],
        help="Control when to print ANSI control characters",
    )
    parser.add_argument(
        "--no-ansi",
        action="store_true",
        help="Do not print ANSI control characters (DEPRECATED)",
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Print version and exit"
    )
    parser.add_argument("-H", "--host", help="Daemon socket to connect to")
    parser.add_argument(
        "--tls", action="store_true", help="Use TLS; implied by --tlsverify"
    )
    parser.add_argument("--tlscacert", help="Trust certs signed only by this CA")
    parser.add_argument("--tlscert", help="Path to TLS certificate file")
    parser.add_argument("--tlskey", help="Path to TLS key file")
    parser.add_argument(
        "--tlsverify", action="store_true", help="Use TLS and verify the remote"
    )
    parser.add_argument(
        "--skip-hostname-check",
        action="store_true",
        help="Don't check the daemon's hostname against the name specified in the client certificate",
    )
    parser.add_argument(
        "--project-directory",
        help="Specify an alternate working directory (default: the path of the Compose file)",
    )
    parser.add_argument(
        "--compatibility",
        action="store_true",
        help="If set, Compose will attempt to convert keys in v3 files to their non-Swarm equivalent (DEPRECATED)",
    )
    parser.add_argument("--env-file", help="Specify an alternate environment file")

    subparsers = parser.add_subparsers(dest="command")
    # subparsers = parser.add_subparsers(dest="command", help="git subcommands")
    for command, help in (
        ("build", "Build or rebuild services"),
        ("config", "Validate and view the Compose file"),
        ("create", "Create services"),
        ("down", "Stop and remove resources"),
        ("events", "Receive real time events from containers"),
        ("exec", "Execute a command in a running container"),
        ("help", "Get help on a command"),
        ("images", "List images"),
        ("kill", "Kill containers"),
        ("logs", "View output from containers"),
        ("pause", "Pause services"),
        ("port", "Print the public port for a port binding"),
        ("ps", "List containers"),
        ("pull", "Pull service images"),
        ("push", "Push service images"),
        ("restart", "Restart services"),
        ("rm", "Remove stopped containers"),
        ("run", "Run a one-off command"),
        ("scale", "Set number of containers for a service"),
        ("start", "Start services"),
        ("stop", "Stop services"),
        ("top", "Display the running processes"),
        ("unpause", "Unpause services"),
        ("up", "Create and start containers"),
        ("version", "Show version information and quit"),
    ):
        subparser = subparsers.add_parser(
            command, add_help=False, prefix_chars=[None], help=help
        )
        subparser.add_argument("arguments", nargs="*")

    return parser.parse_args()


def parse_up_arguments(arguments):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--detach",
        action="store_true",
        default=None,
        help="Detached mode: (default) Run containers in the background, print new container names. Incompatible with --abort-on-container-exit.",
    )
    parser.add_argument(
        "-D",
        "--attached",
        action="store_false",
        default=None,
        dest="detach",
        help="Attached mode: Run containers in the foreground and have no easy way to detach",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Produce monochrome output."
    )

    parser.add_argument(
        "--quiet-pull",
        help="Pull without printing progress information",
        action="store_true",
    )

    parser.add_argument(
        "--no-deps", action="store_true", help="Don't start linked services."
    )
    parser.add_argument(
        "--force-recreate",
        action="store_true",
        help="Recreate containers even if their configuration and image haven't changed.",
    )
    parser.add_argument(
        "--always-recreate-deps",
        action="store_true",
        help="Recreate dependent containers.  Incompatible with --no-recreate.",
    )
    parser.add_argument(
        "--no-recreate",
        action="store_true",
        help="If containers already exist, don't recreate them. Incompatible with --force-recreate and -V.",
    )
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="Don't build an image, even if it's missing.",
    )
    parser.add_argument(
        "--no-start",
        action="store_true",
        help="Don't start the services after creating them.",
    )
    parser.add_argument(
        "--build", action="store_true", help="Build images before starting containers."
    )
    parser.add_argument(
        "--abort-on-container-exit",
        action="store_true",
        help="Stops all containers if any container was stopped. Incompatible with -d.",
    )
    parser.add_argument(
        "--attach-dependencies",
        action="store_true",
        help="Attach to dependent containers.",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        metavar="TIMEOUT",
        help="Use this timeout in seconds for container shutdown when attached or when containers are already running. (default: 10)",
    )
    parser.add_argument(
        "-V",
        "--renew-anon-volumes",
        action="store_true",
        help="Recreate anonymous volumes instead of retrieving data from the previous containers.",
    )
    parser.add_argument(
        "--remove-orphans",
        action="store_true",
        help="Remove containers for services not defined in the Compose file.",
    )
    parser.add_argument(
        "--exit-code-from",
        metavar="SERVICE",
        help="Return the exit code of the selected service container. Implies --abort-on-container-exit.",
    )
    parser.add_argument(
        "--scale",
        metavar="SERVICE=NUM",
        help="Scale SERVICE to NUM instances. Overrides the `scale` setting in the Compose file if present.",
    )
    parser.add_argument("--no-log-prefix", help="Don't print prefix in logs.")

    return parser.parse_args(arguments)


def fail(text):
    print(f"ERROR: {text}", file=sys.stderr)
    sys.exit(1)


def fixDaemon(arguments, detach, sub_arguments):
    if detach == None:
        c_index = len(arguments) - len(sub_arguments)
        return arguments[:c_index] + ["-d"] + sub_arguments

    if not detach:
        rem_index = sub_arguments.index("-D") or sub_arguments.index("--attach")
        if not rem_index:
            fail("Couldn't remove -D, please don't combine it")

        c_index = len(arguments) - len(sub_arguments)
        return (
            arguments[:c_index]
            + sub_arguments[:rem_index]
            + sub_arguments[rem_index + 1 :]
        )

    return arguments


def fixPath(arguments, file):
    if file:
        return arguments

    filenames = [
        "docker-compose.yml",
        "docker-compose.yaml",
        "compose.yml",
        "compose.yaml",
    ]

    first = True
    found = None

    for path in (Path.cwd() / "include-cwd").parents:
        for filename in filenames:
            config = path / filename
            if config.exists():
                if first:
                    return arguments
                found = config
                break
        first = False

    if not found:
        config = os.environ.get("DOCKER_COMPOSE_FILE")
        if config:
            config = Path(config)
            if config.exists():
                found = config

    if not found:
        fail(
            "Cannot find docker-config.  Please place a config file anywhere in this directory\n"
            + f"or parents with name {(', ').join(filenames)}\n"
            + "or set the environment variable DOCKER_COMPOSE_FILE",
        )

    return [arguments[0]] + ["-f", str(found)] + arguments[1:]


def main():
    arguments = sys.argv.copy()

    top = parse_top_arguments()


    if top.command == "up":
        up = parse_up_arguments(top.arguments)
        arguments = fixDaemon(arguments, up.detach, top.arguments)

    arguments = fixPath(arguments, top.file)

    if top.version:
        print(f"Duck Docker Control (ddc) verision {__version__}")
    
    if top.verbose:
        print(f"Calling docker-compose {' '.join(arguments[1:])}")
    os.execvp("docker-compose", arguments)

main()
