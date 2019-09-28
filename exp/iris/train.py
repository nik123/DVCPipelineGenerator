import argparse


def main():
    argparse = parser.ArgumentParser()
    parser.add_argument(
        '--dataset',
        required=True,
        help="Path to file with iris data")
    parser.add_argument(
        '--checkpoint',
        required=True,
        help="Path to store trained model")
    parser.add_argument(
        '--metrics',
        required=True,
        help="Path to store trained model metrics")
    args = parser.parse_args()

    dataset = args.dataset
    checkpoint = args.checkpoint
    metrics = args.metrics

    with open(metrics, 'w') as f:
        print("Test acc.: 100%\n Test loss: 0.0",
              file=f)

    with open(checkpoint, 'w') as f:
        print("1", file=f)


if __name__ == '__main__':
    main()
