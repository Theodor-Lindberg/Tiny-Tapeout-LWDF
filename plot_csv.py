#!/usr/bin/env python3
"""Plot waveform CSV data from cocotb simulation."""

from __future__ import annotations

import argparse
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_waveform(path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"{path} is empty.")
    required = {"cycle", "port_name", "value"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    return df.sort_values("cycle")


def build_signals(df: pd.DataFrame) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    max_cycle = int(df["cycle"].max())
    cycles = np.arange(max_cycle + 1)
    ports = sorted(df["port_name"].unique())
    signals: dict[str, np.ndarray] = {port: np.zeros_like(cycles, dtype=int) for port in ports}

    for row in df.itertuples(index=False):
        signals[row.port_name][row.cycle] = row.value

    return cycles, signals


def plot_signals(cycles: np.ndarray, signals: dict[str, np.ndarray], title: str) -> None:
    print(f"Plotting signals for: {title}")
    fig, axes = plt.subplots(len(signals), 1, figsize=(12, 3 * len(signals)), sharex=True)
    if len(signals) == 1:
        axes = [axes]

    for ax, (name, values) in zip(axes, signals.items()):
        raw = values.astype(np.int64, copy=True)
        max_raw = int(raw.max()) if raw.size else 0
        bit_width = max(1, max_raw.bit_length())
        sign_threshold = 1 << (bit_width - 1)
        if bit_width > 1 and np.any(raw >= sign_threshold):
            raw[raw >= sign_threshold] -= 1 << bit_width
        signals[name] = raw
        values = raw
        ax.stem(cycles, values)
        ax.set_ylabel(name)
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Cycle")
    fig.suptitle(title)
    fig.tight_layout()
    plt.show()

    print("\n=== Waveform Statistics ===")
    print(f"Total cycles: {len(cycles)}")
    for name, values in signals.items():
        print(f"{name}: range [{values.min()}, {values.max()}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot waveform CSV data.")
    parser.add_argument(
        "csv_path",
        type=pathlib.Path,
        nargs="?",
        default=pathlib.Path("src/sim_build/waveform.csv"),
        help="Path to the CSV file.",
    )
    parser.add_argument(
        "--title",
        default="Waveform Plot",
        help="Title for the plot window.",
    )
    args = parser.parse_args()

    if not args.csv_path.exists():
        raise FileNotFoundError(args.csv_path)

    df = load_waveform(args.csv_path)
    cycles, signals = build_signals(df)
    plot_signals(cycles, signals, args.title)


if __name__ == "__main__":
    main()
