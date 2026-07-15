"""
Generate participant aliases for credential distribution.

Usage:
    python workshop-setup/generate_participant_aliases.py --count 200
"""

import argparse
import csv
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate participant aliases such as participant-001."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=200,
        help="Number of aliases to generate. Default: 200.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.count < 1:
        raise SystemExit("--count must be at least 1")

    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["participant_id"])
    for number in range(1, args.count + 1):
        writer.writerow([f"participant-{number:03d}"])


if __name__ == "__main__":
    main()
