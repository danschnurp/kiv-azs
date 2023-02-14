#  date: 15. 01. 2023
#  author: Daniel Schnurpfeil
#

if __name__ == '__main__':
    from audio_cutter import main
    import argparse

    parser = argparse.ArgumentParser(description='audio_cutter')
    parser.add_argument('-i', '--f_input',
                        help='path to input file...', required=True)
    parser.add_argument('-f', '--f_fragment',
                        help='path to input file...', required=True)
    args = parser.parse_args()
    main(args)
