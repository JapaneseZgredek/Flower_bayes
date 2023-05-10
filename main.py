from Flower import Flower

size_setosa = 0
size_versicolor = 0
size_virginica = 0
iris_setosa_correct = 0
iris_setosa_total = 0
iris_virginica_total = 0
iris_virginica_correct = 0
iris_versicolor_total = 0
iris_versicolor_correct = 0

def which_path(chosen_file):
    if chosen_file == 1:
        return r"data/iris_test.txt"
    elif chosen_file == 2:
        return r"data/iris_training.txt"


def read_from_file(chosen_file) -> list:
    list_of_flowers_to_return = []
    path = which_path(chosen_file)

    with open(path, "r") as file:
        read_content = file.read()
        data_in_lines = read_content.split("\n")
        for line in data_in_lines:
            line_as_list = line.split("\t")
            if len(line_as_list) == 1:
                continue
            for i in range(len(line_as_list)):
                line_as_list[i] = line_as_list[i].strip()  # removing white spaces cause University decided to gives us data not only with spaces but also with tabulators :))))
            list_of_flowers_to_return.append(
                Flower(line_as_list[:len(line_as_list) - 1], line_as_list[len(line_as_list) - 1]))  # We know that the last in the list will always be flower type rest is attributes

    return list_of_flowers_to_return


def reformat_data_commas_to_dots(data):
    for flower in data:
        flower.change_commas_to_dots()


def cut_data_into_three_lists(data: list):
    iris_setosa, iris_versicolor, iris_virginica = [], [], []
    for flower in data:
        if flower.flower_type == 'Iris-setosa':
            iris_setosa.append(flower)
        if flower.flower_type == 'Iris-virginica':
            iris_virginica.append(flower)
        if flower.flower_type == 'Iris-versicolor':
            iris_versicolor.append(flower)

    return iris_setosa, iris_versicolor, iris_virginica


def create_dictionaries_for_specific_flower_type(flower_type_list: list) -> list:
    dictionaries_list = [{}, {}, {}, {}]
    for flower in flower_type_list:
        for i in range(len(flower.attributes)):
            if flower.attributes[i] in dictionaries_list[i]:
                dictionaries_list[i][flower.attributes[i]] += 1
            else:
                dictionaries_list[i][flower.attributes[i]] = 1

    return dictionaries_list


def calculate_possibility(dictionaries_of_flower_type: list, flower: Flower, size_of_data: int, size_of_specific_verdict: int, data_dictionaries: list) -> float:
    possibility = size_of_specific_verdict / size_of_data
    for i in range(len(flower.attributes)):
        if flower.attributes[i] in dictionaries_of_flower_type[i]:
            possibility *= (dictionaries_of_flower_type[i][flower.attributes[i]] / size_of_specific_verdict)
        else:
            possibility *= (1/(size_of_specific_verdict+len(data_dictionaries[i])))
    return possibility


def calculate_correctness_of_algorithm(list_of_dictionaries: list, list_of_lists_seperated_by_flower_attributes: list):
    correct_guesses = 0
    what_flower_type = 'Do not know yet'
    for flower in list_of_lists_seperated_by_flower_attributes[3]:
        possibilities = [calculate_possibility(dictionaries_of_flower_type=list_of_dictionaries[0], flower=flower, size_of_data=len(list_of_lists_seperated_by_flower_attributes[3]), size_of_specific_verdict=len(list_of_lists_seperated_by_flower_attributes[0]), data_dictionaries=list_of_dictionaries[3]),
                         calculate_possibility(dictionaries_of_flower_type=list_of_dictionaries[1], flower=flower, size_of_data=len(list_of_lists_seperated_by_flower_attributes[3]), size_of_specific_verdict=len(list_of_lists_seperated_by_flower_attributes[1]), data_dictionaries=list_of_dictionaries[3]),
                         calculate_possibility(dictionaries_of_flower_type=list_of_dictionaries[2], flower=flower, size_of_data=len(list_of_lists_seperated_by_flower_attributes[3]), size_of_specific_verdict=len(list_of_lists_seperated_by_flower_attributes[2]), data_dictionaries=list_of_dictionaries[3])]

        what_flower_type = 'Iris-setosa' if possibilities.index(max(possibilities)) == 0 else \
                           'Iris-virginica' if possibilities.index(max(possibilities)) == 1 else \
                           'Iris-versicolor' if possibilities.index(max(possibilities)) == 2 else 'This should not happen'

        if what_flower_type == flower.flower_type:
            if what_flower_type == 'Iris-setosa':
                global iris_setosa_correct
                global iris_setosa_total
                iris_setosa_correct += 1
                iris_setosa_total += 1
            if what_flower_type == 'Iris-virginica':
                global iris_virginica_correct
                global iris_virginica_total
                iris_virginica_correct += 1
                iris_virginica_total += 1
            if what_flower_type == 'Iris-versicolor':
                global iris_versicolor_correct
                global iris_versicolor_total
                iris_versicolor_correct += 1
                iris_versicolor_total += 1
            correct_guesses += 1
        else:
            if what_flower_type == 'Iris-setosa':
                iris_setosa_total += 1
            if what_flower_type == 'Iris-virginica':
                iris_virginica_total += 1
            if what_flower_type == 'Iris-versicolor':
                iris_versicolor_total += 1

    return correct_guesses, what_flower_type


def main():
    data = read_from_file(1)
    reformat_data_commas_to_dots(data=data)

    iris_setosa, iris_versicolor, iris_virginica = cut_data_into_three_lists(data=data)

    data_dictionary = create_dictionaries_for_specific_flower_type(flower_type_list=data)

    iris_setosa_dictionaries = create_dictionaries_for_specific_flower_type(flower_type_list=iris_setosa)
    iris_versicolor_dictionaries = create_dictionaries_for_specific_flower_type(flower_type_list=iris_versicolor)
    iris_virginica_dictionaries = create_dictionaries_for_specific_flower_type(flower_type_list=iris_virginica)

    correct_guesses, last_flower_type = calculate_correctness_of_algorithm([iris_setosa_dictionaries, iris_virginica_dictionaries, iris_versicolor_dictionaries, data_dictionary], [iris_setosa, iris_virginica, iris_versicolor, data])
    global iris_setosa_total, iris_setosa_correct, iris_versicolor_total, iris_versicolor_correct, iris_virginica_correct, iris_virginica_total
    print(f'Iris-setosa {iris_setosa_correct}/{iris_setosa_total}\n Iris-virginica {iris_virginica_correct}/{iris_virginica_total}\n Iris-versicolor {iris_versicolor_correct}/{iris_versicolor_total}')
    print(str(correct_guesses) + ' --- ' + str(correct_guesses/len(data)))
    does_user_want_to_play = int(input('Do you want to input your own values ? \n0 - Yes\n1 - No\n'))
    while does_user_want_to_play == 0:
        user_attributes = input('Give me ' + str(len(data[0].attributes)) + ' seperated with space and comma as a seperator: ').split(' ')
        for i in range(len(user_attributes)):
            user_attributes[i] = float(user_attributes[i])
        correct_guesses, last_flower_type = calculate_correctness_of_algorithm([iris_setosa_dictionaries, iris_virginica_dictionaries, iris_versicolor_dictionaries, data_dictionary], [iris_setosa, iris_virginica, iris_versicolor, [Flower(user_attributes, '')]])
        print('Your flower is: ' + last_flower_type)
        does_user_want_to_play = int(input('Do you want to input your own values again ? \n0 - Yes\n1 - No\n'))

    print('Thank you for using my Bayes program algorithm')


if __name__ == '__main__':
    main()
