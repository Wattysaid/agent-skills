#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Estimate interview load for a hiring plan.")
    parser.add_argument(
        "--roles",
        required=True,
        help="Comma-separated role names",
    )
    parser.add_argument("--candidates-per-role", type=float, required=True)
    parser.add_argument("--interview-hours", type=float, required=True)
    parser.add_argument("--interviewers", type=float, required=True)
    args = parser.parse_args()

    role_count = len([r for r in args.roles.split(",") if r.strip()])
    total_interviews = role_count * args.candidates_per_role
    total_hours = total_interviews * args.interview_hours
    hours_per_interviewer = total_hours / args.interviewers if args.interviewers else 0

    print("Hiring Plan Load")
    print(f"Roles: {role_count}")
    print(f"Total interviews: {total_interviews:.0f}")
    print(f"Total interview hours: {total_hours:.2f}")
    print(f"Hours per interviewer: {hours_per_interviewer:.2f}")


if __name__ == "__main__":
    main()
