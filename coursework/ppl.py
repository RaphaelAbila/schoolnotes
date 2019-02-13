import re

class Cinema(object):
    """docstring for Cinema."""
        
    def __init__(self):
	##reading prices from another file  ie file        
        file = open('prices.txt','w') 
        file.write('20000\n') 
        file.write('50000\n') 
        file.write('100000\n') 
        file.write('25000\n') 
 
        file.close() 
        file = open('prices.txt', 'r')
        price = file.readlines()

        self.prices = {'Economy':20000,'VIP':50000,'VVIP':100000,'Twin':25000}
        self.seatregex = re.compile(r'([A-P])([0-9]*)')
        self.sold = []
        self.reserved = []
        self.sales = 0
        self.categories =  ['Economy','VIP','VVIP','Twin']
        self.seatsCategories = { self.categories[3]:{'seats':[range(4,15)], 'rows':range(2)},
                                self.categories[2]:{'seats':[range(4),range(15,20)],'rows':range(2),'extra_seats':range(20),'extra_rows':range(2,6)},
                                self.categories[1]:{'seats':[range(20)],'rows':range(6,12)},
                                self.categories[0]:{'seats':[range(20)],'rows':range(12,16)}}
        self.seats = []
        self.number_of_seats=0
        self.populate_seats()
        self.display_seats()

	##displaying seating chart
    def populate_seats(self):
        self.seats = [['*']*20 for n in range(16)]
        return 0

    def display_seats(self):
        row_num = 65
        print('\t    1\t 2    3    4    5    6    7    8    9    10   11   12   13  14   15   16   17   18   19   20')
        for row in self.seats:

            print('\t'+chr(row_num) + ' | ' + ' |  '.join(row)+ ' |')
            row_num = row_num + 1

        print('\nSCREEN')
        print('Number of seats available:' + str(self.available_seats()))
        print('Total sales: shs.' + str(self.sale()))


		## decision making to reserve with payment or not
        action = input('Choose Action (C for continue,any character for Exit:)')
        if action == 'C':
            return self.sale_prompt()
        else:
            return exit()

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
            self.number_of_seats = 0

            return self.handle_sales(choice,category)

        else:
            print('No seats are reserved yet!')
            return self.display_seats()

    def sale_prompt(self):
        try:
            self.number_of_seats = input('\nEnter number of seats required:')
        except Exception as e:
            print('Please enter the correct input')
            self.sale_prompt()
        else:

            if int(self.number_of_seats) > 0:
                desired_category = input("\nDesired seat category(Twin, VVIP, VIP or Economy): ")
                if desired_category in self.categories:
                    available = self.available_in_category(desired_category)
                    if int(self.number_of_seats) <= len(available):
                        for seat in available:
                            print(seat,self.get_CategoryPrice(desired_category))
                    else:
                        print('Available seats for ' + desired_category + ':' + str(len(available)))
                        return self.sale_prompt()
                    try:
                       
                        chosen_seat = input('\n Choose Seat please (eg C7):  ')
                    except Exception as e:
                        print('Please check the seat format')
                        return self.sale_prompt()

                    else:
                        try:
                            if chosen_seat in available:
                                choice = input('Press C for Cash or B for reservation/booking without cash: ')
                                if choice == 'C':
                                    return self.handle_sales(chosen_seat,desired_category)
                                elif choice == 'B':
                                    return self.handle_reservations(chosen_seat,desired_category)
                                else:
                                    print('Please enter B or C !!!!')
                                    return self.sale_prompt()


                            else:
                                raise Exception('Seat Not available')

                        except Exception as e:
                            print(str(e) + '\n')
                            return self.sale_prompt()
                else:
                    print(' Please enter the correct format next time!!!!!')
            else:
                print('Thats not proper-----')
                self.sale_prompt()


    def available_in_category(self,category):
            no_of_seats = []
            category_details = self.seatsCategories[category]

            for row in category_details['rows']:
                for range  in category_details['seats']:
                    for seat in range:
                        if self.seats[row][seat] == '*':
                            no_of_seats.append(str(chr(65 + row)) + str(seat + 1))

            if 'extra_rows' in category_details:
                for row in category_details['extra_rows']:
                    for seat in category_details['extra_seats']:
                        if self.seats[row][seat]=='*':
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
            if categoryprice == 0:
                raise Exception('Seat Does Not Exist Please.')

            if category == 'Twin':
                
                if seat in self.reserved:
                    del self.reserved[self.reserved.index(seat) + 1]

                self.handle_sales_twin(raw,int(seatNo))
                return self.display_seats()
            else:
               
                self.handle_sit_sales(categoryprice,raw,int(seatNo),category,'normal')
                return self.display_seats()

        else:
            raise Exception('Seat or Category Does Not Exist:')



    def handle_sit_sales(self,categoryprice,raw,seat,category,code):
    	if code == 'normal':
    		list_of_seats = self.available_in_category(category)
    		real_seat = str(raw + str((seat)))
    		index = list_of_seats.index(real_seat)
    		sales_array = []
    		for n in range(index,(index + int(self.number_of_seats))):
    			sales_array.append(list_of_seats[n])
    		for seatn in sales_array:
    			raw,seatNo = (self.seatregex.search(seatn)).groups()
    			real_raw = (ord(raw)-65)
    			self.seats[real_raw][(int(seatNo)-1)] = '#'
    			self.sold.append(raw + str(seatNo))
    			self.sales = self.sales + (categoryprice)
    	return 0



    def handle_sales_twin(self,raw,seat):
    		list_of_seats = self.available_in_category('Twin')
    		real_seat = str(raw + str((seat)))

    		index = list_of_seats.index(real_seat)
    		sales_array = []
    		try:
	    		for n in range(index,(index + (int(self.number_of_seats)*2))):
	    			sales_array.append(list_of_seats[n])
	    		for seatn in sales_array:
	    			raw,seatNo = (self.seatregex.search(seatn)).groups()
	    			real_raw = (ord(raw)-65)
	    			if self.seats[real_raw][(int(seatNo)-1)] == '#' :
	    				continue
	    			else:
	    				
		    			self.seats[real_raw][(int(seatNo)-1)] = '#'
		    			self.sold.append(raw + str(seatNo))
		    			
		    			if int(seatNo)==15:
		    				raw,seatNo = (self.seatregex.search(sales_array[(sales_array.index(seatn)+1)])).groups()
			    			self.seats[(ord(raw)-65)][(int(seatNo)-1)] = '#'
			    			self.sold.append(raw + str(int(seatNo)))
			    			self.sales = self.sales + (2*25000)
			    		else:	
			    			self.seats[real_raw][(int(seatNo))] = '#'
			    			self.sold.append(raw + str(int(seatNo)+1))
			    			self.sales = self.sales + (2*25000)
		    				


    		except Exception as e:
    			print('No of seats needed is too much')
    		return 0

    def handle_reservations(self,seat,category):
        checkseat = self.seatregex.search(seat)
        if checkseat is not None:
            raw,seatNo = checkseat.groups()
            #categoryprice = self.get_CategoryPrice(category) if (int(seatNo) < 21 and int(seatNo) > 0) else 0
            if category == 0:
                raise Exception('Seat Does Not Exist Please.')

            if category == 'Twin':
                
                self.handle_reservations_twin(raw,int(seatNo))
                return self.display_seats()
            else:
               
                self.handle_sit_reservation(raw,int(seatNo),category)
                return self.display_seats()

        else:
            raise Exception('Seat Does Not Exist:')

#Reserving a twin seat
    def handle_reservations_twin(self,raw,seat):
    		list_of_seats = self.available_in_category('Twin')
    		real_seat = str(raw + str((seat)))

    		index = list_of_seats.index(real_seat)
    		sales_array = []
    		try:
	    		for n in range(index,(index + (int(self.number_of_seats)*2))):
	    			sales_array.append(list_of_seats[n])
	    		for seatn in sales_array:
	    			raw,seatNo = (self.seatregex.search(seatn)).groups()
	    			real_raw = (ord(raw)-65)
	    			if self.seats[real_raw][(int(seatNo)-1)] == 'a' :
	    				continue
	    			else:
	    				
		    			self.seats[real_raw][(int(seatNo)-1)] = 'a'
		    			self.sold.append(raw + str(seatNo))
		    			
		    			if int(seatNo)==15:
		    				raw,seatNo = (self.seatregex.search(sales_array[(sales_array.index(seatn)+1)])).groups()
			    			self.seats[(ord(raw)-65)][(int(seatNo)-1)] = 'a'
			    			self.sold.append(raw + str(int(seatNo)))
			    
			    		else:	
			    			self.seats[real_raw][(int(seatNo))] = 'a'
			    			self.sold.append(raw + str(int(seatNo)+1))
			    			
		    				


    		except Exception as e:
    			print('No of seats needed is too much')
    		return 0


#Reserving other seats
    def handle_sit_reservation(self,raw,seat,category):
    		list_of_seats = self.available_in_category(category)
    		real_seat = str(raw + str((seat)))
    		index = list_of_seats.index(real_seat)
    		sales_array = []
    		for n in range(index,(index + int(self.number_of_seats))):
    			sales_array.append(list_of_seats[n])
    		for seatn in sales_array:
    			raw,seatNo = (self.seatregex.search(seatn)).groups()
    			real_raw = (ord(raw)-65)
    			self.seats[real_raw][(int(seatNo)-1)] = 'a'
    			self.reserved.append(raw + str(seatNo))

    		return 0

    def get_CategoryPrice(self,category):
        return self.prices[category]

new = Cinema()
