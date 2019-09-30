import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data',
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
    parser.add_argument('--epochs', required=True)
    args = parser.parse_args()

    data = args.data
    checkpoint = args.checkpoint
    metrics = args.metrics
    epochs = args.epochs

    # No real training. Just simulate training process:
    with open(metrics, 'w') as f:
        print("Test acc.: 100%\n Test loss: 0.0",
              file=f)
    with open(checkpoint, 'w') as f:
        print("1", file=f)


if __name__ == '__main__':
    main()
