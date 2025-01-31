from motus import Attempt, Answer, Color

def get_color_input():
    color_input = input("Entrez les couleurs (R pour rouge, J pour jaune, etc.) : ")
    color_map = {'R': Color.RED, 'J': Color.YELLOW, 'B': Color.BLUE}  # Ajoutez d'autres couleurs si nécessaire
    return [color_map[char] for char in color_input]

def main():
    word = input("Entrez un mot : ")
    colors = get_color_input()
    answer = Answer(*colors)
    attempt = Attempt(word, answer)
    print(attempt)

if __name__ == "__main__":
    main()