from s2p_to_yaksi_datastructure.DataStructureTransform import Transform_results
import argparse


def main():
    parser = argparse.ArgumentParser(description="Process suite2p processed data folder path.")
    parser.add_argument("data_path", type=str, help="Path to the suite2p data folder")
    parser.add_argument(
        "--save_format",
        type=str,
        choices=["mat", "npy"],
        default="mat",
        help="Format to save results (default: mat)",
    )
    args = parser.parse_args()

    results_obj = Transform_results(args.data_path, args.save_format == "mat")
    if args.save_format == "mat":
        results_obj.save_as_mat()
    else:
        results_obj.save_as_npy()


if __name__ == "__main__":
    main()
