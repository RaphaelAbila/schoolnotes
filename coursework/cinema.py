import re

class Cinema(object):
    """docstring for Cinema."""

    def __init__(self):
        self.prices = {'Economy':20000,'VIP':50000,'VVIP':100000,'Twin':25000}
        self.seatregex = re.compile(r'([A-P])([0-9]*)')
        self.sold = []
        self.reserved = []
        self.sales = 0
        self.categories =  ['Economy','VIP','VVIP','Twin']
        self.seatsCategories = { self.categories[3]:{'seats':[range(4,15)], 'rows':range(2)},
                                self.categories[2]:{'seats':[range(5),range(15,20)],'rows':range(2),'extra_seats':range(20),'extra_rows':range(2,6)},
                                self.categories[1]:{'seats':[range(20)],'rows':range(6,12)},
                                self.categories[0]:{'seats':[range(20)],'rows':range(12,16)}}
        self.seats = []
        self.populate_seats()
        self.display_seats()

##displaying seating chart
    def populate_seats(self):
        self.seats = [['*']*20 for n in range(16)]
        return 0

    def display_seats(self):
        row_num = 65

        for row in self.seats:

            print('\t'+chr(row_num) + ' | ' + ' |  '.join(row)+ ' |')
            row_num = row_num + 1

        print('\nSCREEN')
        print('Number of seats available:' + str(self.available_seats()))
        print('Total sales: shs.' + str(self.sale()))


## decision making to reserve with payment or not
        action = input('Choose Action (C for continue, B for paying Reserved Seats, any character for Exit:)')
        if action == 'C':
            return self.sale_prompt()
        elif action == 'B':
            return self.pay_for_reserved()
        else:
            return exit()

    print('\t    1\t 2    3    4    5    6    7    8    9    10   11   12   13  14   15   16   17   18   19   20')
##seat reservation
    def seat_no(self):
        seats = []
        for i in range(20):
            seats.append(str(i))
        return seats

##Available seats
    def available_seats(self):
        return (len(self.seats)*20)-len(self.sold)-len(self.reserved)

    def sale(self):
        return self.sales

##Paying a reserved seat of a particular category
    def pay_for_reserved(self):
        if self.reserved:
            for seat in self.reserved:
                print(seat)
            choice = input('Enter seat:  ')
            category = input('\nEnter seat category:  ')

            return self.handle_sales(choice,category)

        else:
            print('No seats are reserved yet!')
            return self.display_seats()

    def sale_prompt(self):
        try:
            number_of_seats = input('\nEnter number of seats required:')
        except Exception as e:
            print('What have you done')
            self.sale_prompt()
        else:

            if int(number_of_seats) > 0:
                desired_category = input("\nDesired seat category(Twin, VVIP, VIP or Economy): ")
                if desired_category in self.categories:
                    available = self.available_in_category(desired_category)
                    if int(number_of_seats) <= len(available):
                        for seat in available:
                            print(seat,self.get_CategoryPrice(desired_category))
                    else:
                        print('Available seats for ' + desired_category + ':' + str(len(available)))
                        return self.sale_prompt()
                    try:
                        chosen_seat = input('\n Choose Seat please (eg C7):  ')
                    except Exception as e:
                        print('but wats wrong with you')
                        return self.sale_prompt()

                    else:
                        try:
                            if chosen_seat in available:
                                choice = input('Press C for Cash or B for reservation/booking: ')
                                if choice == 'C':
                                    return self.handle_sales(chosen_seat,desired_category)
                                elif choice == 'B':
                                    return self.handle_reservations(chosen_seat,desired_category)
                                else:
                                    print('you are warned !!!!')
                                    return self.sale_prompt()


                            else:
                                raise Exception('Seat Not available')

                        except Exception as e:
                            print(str(e) + '\n')
                            return self.sale_prompt()
                else:
                    print(' u degenerate scum!!!!!')
            else:
                print('Thats not proper-----')
                self.sale_prompt()


    def available_in_category(self,category):
            no_of_seats = []
            category_details = self.seatsCategories[category]
            if 'extra_rows' in category_details:
                for row in category_details['extra_rows']:
                    for seat in category_details['extra_seats']:
                        if self.seats[row][seat]=='*':
                            no_of_seats.append(str(chr(65 + row)) + str(seat + 1))

            for row in category_details['rows']:
                for range  in category_details['seats']:
                    for seat in range:
                        if self.seats[row][seat] == '*':
                            no_of_seats.append(str(chr(65 + row)) + str(seat + 1))

            return no_of_seats

##seat sales
    def handle_sales(self, seat,category):
        if seat in self.reserved:
            del self.reserved[self.reserved.index(seat)]
        checkseat = self.seatregex.search(seat)
        if checkseat is not None and category in self.categories:
            raw,seatNo = checkseat.groups()
            categoryprice = self.get_CategoryPrice(category) if (int(seatNo) < 21 and int(seatNo) > 0) else 0
            if category == 0:
                raise Exception('Seat Does Not Exist Please.')

            if category == 'Twin' and int(seatNo) is not 15:
                print('seats to be sold:' + raw + str(seatNo) + ' and ' + raw + str(int(seatNo)+ 1))
                if seat in self.reserved:
                    del self.reserved[self.reserved.index(seat) + 1]

                self.handle_sales_twin(raw,int(seatNo))
                return self.display_seats()
            else:
                print('seats to be sold:' + raw + str(seatNo))
                self.handle_sit_sales(categoryprice,raw,int(seatNo))
                return self.display_seats()

        else:
            raise Exception('Seat or Category Does Not Exist:')



    def handle_sit_sales(self,categoryprice,raw,seat):
            real_raw = (ord(raw)-65)

            self.seats[real_raw][seat-1] = '#'
            self.sold.append(raw + str(seat))

            self.sales = self.sales + (1*categoryprice)

            return 0



    def handle_sales_twin(self,raw,seat):
        real_raw = (ord(raw)-65)

        self.seats[real_raw][seat-1] = '#'
        self.sold.append(raw + str(seat))

        self.seats[real_raw][seat] = '#'
        self.sold.append(raw + str(seat + 1))

        self.sales = self.sales + (2*25000)


        return 0

    def handle_reservations(self,seat,category):
        checkseat = self.seatregex.search(seat)
        if checkseat is not None:
            raw,seatNo = checkseat.groups()
            categoryprice = self.get_CategoryPrice(category) if (int(seatNo) < 21 and int(seatNo) > 0) else 0
            if category == 0:
                raise Exception('Seat Does Not Exist Please.')

            if category == 'Twin' and int(seatNo) is not 15:
                print('seats to be reserved:  ' + raw + str(seatNo) + ' and ' + raw + str(int(seatNo)+ 1))
                self.handle_reservations_twin(raw,int(seatNo))
                return self.display_seats()
            else:
                print('seat to be reserved:  ' + raw + str(seatNo))
                self.handle_sit_reservation(raw,int(seatNo))
                return self.display_seats()

        else:
            raise Exception('Seat Does Not Exist:')

#Reserving a twin seat
    def handle_reservations_twin(self,raw,seat):
            real_raw = (ord(raw)-65)

            self.seats[real_raw][seat-1] = '#'
            self.reserved.append(raw + str(seat))

            self.seats[real_raw][seat] = '#'
            self.reserved.append(raw + str(seat + 1))

            print('Seats Successfully reserved ')

            return 0

#Reserving other seats
    def handle_sit_reservation(self,raw,seat):
                real_raw = (ord(raw)-65)

                self.seats[real_raw][seat-1] = '#'
                self.reserved.append(raw + str(seat))

                print('Seat Successfully reserved')
                return 0

    def get_CategoryPrice(self,category):
        return self.prices[category]

new = Cinema()
