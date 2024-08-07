import sys, pathlib, cv2, argparse, math

class ThresholdingException(Exception):
    pass

def calculate_threshold(image1_path, image2_path, 
                        dimensionX=None, dimensionY=None, queue=None):
    input_path1 = str(image1_path.resolve())
    img1 = cv2.imread(input_path1, cv2.IMREAD_GRAYSCALE)

    input_path2 = str(image2_path.resolve())
    img2 = cv2.imread(input_path2, cv2.IMREAD_GRAYSCALE)

    if dimensionX and dimensionY:
        col_start, col_end = dimensionX
        row_start, row_end = dimensionY
    else:
        x, y, w, h = cv2.selectROI(img1)
        cv2.destroyAllWindows()
        col_start = x
        col_end = x + w
        row_start = y
        row_end = y + h

    if col_end - col_start == 0 or row_end - row_start == 0:
        raise ThresholdingException("Invalid region select again")
    differences = []
    for column in range(min(col_start, col_end), max(col_start, col_end)):
        for row in range(min(row_start, row_end), max(row_start, row_end)):
            first_frame_area = int(img1[row][column])
            second_frame_area = int(img2[row][column])
            diff = abs(first_frame_area - second_frame_area)
            differences.append(diff)
    threshold = math.ceil(sum(differences)/len(differences))
    print(f"Threshold Amount: {threshold}")
    if queue is not None:
        queue.put(f"Threshold Amount: {threshold}")
    return threshold

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
         usage="%(prog)s [-h] [-v] -p1 PATH1 -p2 PATH2 [-x X_TUPLE -y Y_TUPLE]", 
         add_help=False,
        description="Calculates threshold value used in combine_images based off regions of 2 frames. Note: Both -x and -y must be provided together or not at all."
    )

    required = parser.add_argument_group('required arguments')
    required.add_argument("-p1", "--path1", action="store", type=pathlib.Path, required=True,
        help = "Full path to first frame")
    required.add_argument("-p2", "--path2", action="store", type=pathlib.Path, required=True,
        help = "Full path to second frame")
    
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-h", "--help", action="help", 
                          help="show this help message and exit")
    optional.add_argument("-v", "--version", action="version", 
                        version=f"{parser.prog} version 1.0.0")
    optional.add_argument("-x", "--dimensionX", type=tuple_type, 
                        help = "X dimensions used in calculation (format: '(x1,x2)')")
    optional.add_argument("-y", "--dimensionY", type=tuple_type,
                        help = "Y dimensions used in calculation (format: '(y1,y2)')")
    return parser

def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped_int = map(int, strings.split(","))
    return tuple(mapped_int)

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if (args.dimensionX is None) != (args.dimensionY is None):
        parser.error("Both --dimension1 and --dimension2 must be provided together or not at all.")
        
    try:
        calculate_threshold(args.path1, args.path2, args.dimensionX, 
                            args.dimensionY)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()