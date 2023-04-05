class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        output = str(self.feet) + ' feet, ' + str(self.inches) + ' inches'
        return output

    def __add__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        total_height_inches = height_A_inches + height_B_inches
        output_feet = total_height_inches // 12
        output_inches = total_height_inches - (output_feet * 12)
        return Height(output_feet, output_inches)

    def __sub__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        difference__height__inches = height_A_inches - height_B_inches
        output__feet = difference__height__inches // 12
        output__inches = difference__height__inches - (output__feet * 12)

        return Height(output__feet, output__inches)

    def __lt__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches < height_B_inches

    def __le__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches <= height_B_inches

    def __eq__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches == height_B_inches

    def __gt__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches > height_B_inches

    def __ge__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches >= height_B_inches

    def __ne__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches != height_B_inches


# person_A_height = Height(5, 10)
# person_B_height = Height(4, 10)
# height_sum = person_A_height + person_B_height
# print('Total height:', height_sum)

# person_A_height = Height(5, 10)
# person_B_height = Height(4, 10)
# height_sub = person_A_height - person_B_height
# print('Difference of Person A\'s height and Person B\'s height:', height_sub)

print('Height(4, 6) > Height(4, 5) is:', Height(4, 6) > Height(4, 5))
print('Height(4, 5) >= Height(4, 5) is:', Height(4, 5) >= Height(4, 5))
print('Height(5, 9) != Height(5, 10) is:', Height(5, 9) != Height(5, 10))
