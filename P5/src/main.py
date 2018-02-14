import argparse
from PathPlanning import PathPlanning


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Path Planning')
    parser.add_argument('input_file', type=str, help='name of the input file.')
    parser.add_argument('output_file', type=str, default=None, help='name for the output file.')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    PP = PathPlanning(input_file)
    PP.dynamic_programming()
    PP.generate_path(output_file)