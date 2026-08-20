from __future__ import annotations

import argparse

from klas_model.collectors.cli import fetch_cli_history, save_cli_history


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill official KPHX NWS CLIPHX daily highs from the IEM text archive"
    )
    parser.add_argument("--start", required=True, help="First KPHX climate date, YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Last KPHX climate date, YYYY-MM-DD")
    parser.add_argument("--output", default="data/raw/cli/kphx_cli_daily.csv")
    args = parser.parse_args()

    df = fetch_cli_history(args.start, args.end)
    save_cli_history(df, args.output)

    final_count = int(df.get("cli_is_final", []).sum()) if not df.empty else 0
    preliminary_count = len(df) - final_count
    print(f"saved {len(df):,} CLI daily rows to {args.output}")
    print(f"final YESTERDAY reports: {final_count:,}")
    if preliminary_count:
        print(
            f"preliminary-only TODAY rows: {preliminary_count:,} "
            "(these will not be used as settlement targets)"
        )


if __name__ == "__main__":
    main()
