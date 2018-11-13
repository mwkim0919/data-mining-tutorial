import argparse
import colorama
from tabulate import tabulate

colorama.init(autoreset=True)

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }


def printDataSet(users: dict) -> None:
  headers = ['Users', 'Blues Traveler', 'Broken Bells', 'Deadmau5', 'Norah Jones',
            'Phoenix', 'Slightly Stoopid', 'The Strokes', 'Vampire Weekend']
  # minifiedHeaders = ['Users', 'B.T.', 'B.B.', 'Deadmau5', 'N.J.',
  #                   'Phoenix', 'S.S.', 'The Strokes', 'V.W.']
  userRatings = []
  for user in users.keys():
    rating = []
    rating.append(user)
    for index in range(1, len(headers)):
      if headers[index] in users[user]:
        rating.append(users[user][headers[index]])
      else:
        rating.append(None)
    userRatings.append(rating)
  print(tabulate(userRatings, headers))


def manhattan(user1: dict, user2: dict) -> float:
  """
  Compute the Manhattan distance. (difference in x and y)
  :return: Manhattan distance
  """
  distance = 0
  for artist in user1:
    if artist in user2:
      distance += abs(user1[artist] - user2[artist])
  return distance


def computeNearestNeighbor(username: str, users: dict) -> list:
  """
  Create a sorted list of users based on their distance to username
  :return: list of users with similar preference
  """
  distances = []
  for user in users:
    if user != username:
      distance = manhattan(users[user], users[username])
      distances.append((distance, user))
  distances.sort()
  # print(distances)
  return distances


def recommend(username: str, users: dict) -> list:
  """
  Give list of recommendations.
  :return: list of artist recommendation
  """
  nearest = computeNearestNeighbor(username, users)[0][1]
  recommendations = []
  neighborRatings = users[nearest]
  userRatings = users[username]
  for artist in neighborRatings:
    if not artist in userRatings:
      recommendations.append((artist, neighborRatings[artist]))
  return sorted(recommendations,
                key=lambda artistTuple: artistTuple[1],
                reverse = True)


def main():
  """Parse arguments."""
  parser = argparse.ArgumentParser()
  parser.add_argument('user',
                    help='Provide one of the user: {' + ' '.join(users.keys()) + '}')
  args = parser.parse_args()
  printDataSet(users)
  print(colorama.Fore.YELLOW + args.user + '\'s Artist Recommendation: ')
  print(colorama.Fore.GREEN + str(recommend(args.user, users)))


if __name__ == '__main__':
  main()

