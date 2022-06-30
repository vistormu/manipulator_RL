import matplotlib.pyplot as plt
import pandas


def main():

    filename = "results/results.csv"

    data = pandas.read_csv(filename)

    episodes = data['episode'].to_numpy()
    steps = data['steps'].to_numpy()
    rewards = data['rewards'].to_numpy()
    dones = data['done'].to_numpy()

    plt.scatter(episodes, dones, marker='x', color="#b64545")
    plt.show()


if __name__ == '__main__':
    main()
