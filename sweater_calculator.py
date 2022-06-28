# dictionary with your measurements + reglan_stitches to decide
your_measurements = {'sample': {'width': 20, 'height': 10, 'w_stitches': 36, 'h_rows': 24, 'reglan_stitches': 2}, \
                     'sweater': {'neck': 50, 'bust_half': 38, 'under_arm_half': 12.5, 'length_total': 44, \
                                 'length_bottom_to_armpit': 25, 'sleeve_wrist_to_armpit': 29, 'sleeve_wrist_half': 11,
                                 'neckopening_height': 5}}
reglan = int(your_measurements['sample']['reglan_stitches'])


# measurements to stitches and rows
def measurements_recalculation(measurements):
    result = {'neck': round(
        (measurements['sweater']['neck'] * measurements['sample']['w_stitches']) / measurements['sample']['width']),
        'bust': round(
            (measurements['sweater']['bust_half'] * 2 * measurements['sample']['w_stitches']) / measurements['sample'][
                'width']),
        'under_arm': round(
            (measurements['sweater']['under_arm_half'] * 2 * measurements['sample']['w_stitches']) /
            measurements['sample'][
                'width']),
        'length_total': round(
            (measurements['sweater']['length_total'] * measurements['sample']['h_rows']) / measurements['sample'][
                'height']),
        'length_bottom_to_armpit': round(
            (measurements['sweater']['length_bottom_to_armpit'] * measurements['sample']['h_rows']) /
            measurements['sample']['height']),
        'length_top_to_armpit': round(((measurements['sweater']['length_total'] - measurements['sweater'][
            'length_bottom_to_armpit']) * measurements['sample']['h_rows']) / measurements['sample']['height']),
        'sleeve_wrist_to_armpit': round(
            (measurements['sweater']['sleeve_wrist_to_armpit'] * measurements['sample']['h_rows']) /
            measurements['sample'][
                'height']),
        'sleeve_wrist': round(
            (measurements['sweater']['sleeve_wrist_half'] * 2 * measurements['sample']['w_stitches']) /
            measurements['sample'][
                'width']),
        'reglan_stitches_total': measurements['sample']['reglan_stitches'] * 4,
        'neckopening_height': round(
            (measurements['sweater']['neckopening_height'] * measurements['sample']['h_rows']) / measurements['sample'][
                'height'])}

    return result


row_stitch_measurements = measurements_recalculation(your_measurements)


# finding marker points
def marker_points(r_s_measure):
    markers = []

    sleeve_part = 1
    front_part = round(((r_s_measure['bust'] / 2) / r_s_measure['under_arm']), 2)
    total_parts = 2 * (sleeve_part + front_part)
    one_part = round((r_s_measure['neck'] - r_s_measure['reglan_stitches_total']) / total_parts)
    sleeve = one_part + reglan
    front_back = round((one_part * front_part) + reglan)
    opening_give = round(front_back / 4.5)
    front = front_back + opening_give
    back = front_back - opening_give

    marker_1 = round(front / 2)
    til_end = r_s_measure['neck'] - (marker_1 + 2 * sleeve + back)
    if (marker_1 + til_end) % 2 == 0:
        markers.append(int((marker_1 + til_end) / 2))

    markers.append(markers[0] + sleeve)
    markers.append(markers[1] + back)
    markers.append(markers[2] + sleeve)
    markers.append(r_s_measure['neck'] - markers[3])

    return markers, sleeve, back


markers, sleeve, back = marker_points(row_stitch_measurements)


# calculate turnarounds in neck part
def turnarounds(r_s_measure):
    total_turns = r_s_measure['neckopening_height'] / 2
    sleeve_turns = round(r_s_measure['neckopening_height'] / 3)
    turn_freq_stitches = round((sleeve - r_s_measure['reglan_stitches_total'] / 4) / (sleeve_turns + 1))

    return total_turns, sleeve_turns, turn_freq_stitches


total_turns, sleeve_turns, turn_freq_stitches = turnarounds(row_stitch_measurements)


# neck
def neck(markers, sleeve_part, back_part, your_measurements, total_turns, turn_freq_stitches):
    reg_line = your_measurements['sample']['reglan_stitches']
    front_half = int(markers[0] - (reg_line / 2))
    sleeve = int(sleeve_part - reg_line)
    back = int(back_part - reg_line)
    yarn_over = 1
    increase = turn_freq_stitches
    row_end = increase
    turns_count = total_turns
    marker_distance = sleeve
    end_distance = front_half
    neck_description = []

    for row in range(1, int(total_turns) * 2 + 1):
        if increase < marker_distance:
            if row == 1:
                neck_description.append(
                    f"[Row {row}]: knit front half {front_half} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + sleeve {sleeve} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + back {back} +  yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + knit {row_end} -> Turn")
                row_end += 1
                back += 2
                turns_count -= 1
                marker_distance -= increase
            elif row % 2 == 0:
                neck_description.append(
                    f"[Row {row}]: knit {row_end} + reglan line {reg_line} + back {back} + reglan line {reg_line} + knit {row_end} -> Turn")
            else:
                neck_description.append(
                    f"[Row {row}]: knit {row_end} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + back {back} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + knit {row_end + increase} -> Turn")
                row_end += increase + 1
                back += 2
                turns_count -= 1
                marker_distance -= increase
                increase += 1

        elif increase > marker_distance > 0:
            if row % 2 == 0:
                neck_description.append(
                    f"[Row {row}]: knit {row_end} + reglan line {reg_line} + back {back} + reglan line {reg_line} + knit {row_end} -> Turn")
            else:
                neck_description.append(
                    f"[Row {row}]: knit {row_end} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + back {back} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + knit sleeve {row_end + marker_distance} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + knit {increase - marker_distance} -> Turn")
                sleeve = row_end + marker_distance + reg_line
                row_end = increase - marker_distance + 1
                back += 2
                turns_count -= 1
                marker_distance -= increase
                increase += 1
                end_distance -= row_end
                if marker_distance < 0:
                    marker_distance = 0

        else:
            if row % 2 == 0:
                neck_description.append(
                    f"[Row {row}]: knit {row_end} + reglan line {reg_line} + sleeve {sleeve} + reglan line {reg_line} + back {back} + reglan line {reg_line} + sleeve {sleeve} + reglan line {reg_line} + knit {row_end} -> Turn")
            else:
                neck_description.append(
                    f"[Row {row}]: knit {row_end} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + sleeve {sleeve} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + back {back} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + sleave {sleeve} + yarn over {yarn_over} + reglan line {reg_line} + yarn over {yarn_over} + knit {row_end + increase} -> Turn")
                row_end += increase + 1
                back += 2
                sleeve += 2
                turns_count -= 1
                end_distance -= increase
                increase += 1

    last_neck_row = int(total_turns) * 2 + 1
    total_stitches_after_neck = 2 * row_end + 2 * end_distance + 2 * sleeve + back + 4 * reg_line

    neck_description.append(
        f"[Row {last_neck_row}]: knit {row_end} + reglan line {reg_line} + sleave {sleeve} + reglan line {reg_line} + back {back} + reglan line {reg_line} + sleave {sleeve} + reglan line {reg_line} + knit {row_end + end_distance}")
    neck_description.append('_______________________________________________________________________________')
    neck_description.append(
        "You should reach end of stitches line.\nNow your sweater will be worked in the circle! In the next Row attach last stitch to the first stitch!")
    neck_description.append(f'You have total of {total_stitches_after_neck} stiches at [Row {last_neck_row}].')

    return total_stitches_after_neck, last_neck_row, sleeve, neck_description


total_stitches_after_neck, last_neck_row, sleeve_at_neck, neck_description = neck(markers, sleeve, back, your_measurements, total_turns, turn_freq_stitches)


def regular_increase(total_stitches_after_neck, last_neck_row, row_stitch_measurements):
    total_stitches_under_arm = row_stitch_measurements['bust'] + 2 * row_stitch_measurements['under_arm']
    rows_count = row_stitch_measurements['length_top_to_armpit'] - last_neck_row
    increase_count = round((total_stitches_under_arm - total_stitches_after_neck) / 8)
    row_list_inc = list(range(last_neck_row + 1, row_stitch_measurements['length_top_to_armpit'] + 1))

    return row_list_inc, increase_count


row_list_inc, increase_count = regular_increase(total_stitches_after_neck, last_neck_row, row_stitch_measurements)


# splitting list into N parts of approximately equal length
def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


increase_row_number = []
for chunk in chunk_it(row_list_inc, increase_count):
    increase_row_number.append(chunk[0])

total_stitches_before_bust = total_stitches_after_neck + increase_count * 8

sleeve_disconnected = sleeve_at_neck + 2 * increase_count + reglan
total_stitches_bust = total_stitches_before_bust - 2 * (sleeve_disconnected) + 2 * 8
first_row_bust = row_list_inc[-1] + 1
rows_until_bottom = first_row_bust + row_stitch_measurements['length_bottom_to_armpit']


# arm decrease
def regular_decrease(total_stitches_after, last_row, row_stitch_measurements):
    rows_count = last_row + row_stitch_measurements['sleeve_wrist_to_armpit']
    decrease_count = round((total_stitches_after - row_stitch_measurements['sleeve_wrist']) / 2)
    row_list_dec = list(range(last_row + 1, rows_count + 1))

    return row_list_dec, decrease_count


row_list_dec, decrease_count = regular_decrease(sleeve_disconnected, first_row_bust, row_stitch_measurements)

decrease_row_number = []
for chunk in chunk_it(row_list_dec, decrease_count):
    decrease_row_number.append(chunk[0])

total_stitches_wrist = sleeve_disconnected - decrease_count * 2

# printing results
print(
    f"Start by casting on {row_stitch_measurements['neck']} stitches.\nPlace markers after stitch: {markers[0:-1]}. They will be in the middle of your reglan lines.")
print('____________________________________________________\n____________________________________________________')
print('Working on the neck opening:\n________________________________________________________')
for description in neck_description:
    print(description)
print('____________________________________________________\n____________________________________________________')
print('Working from the neck to armpits:\n________________________________________________________')
print(
    f'Knit in the circle until [Row {row_list_inc[-1]}] (included) and increase 1 stich around every reglan line in Row: {increase_row_number}, (total increase in 1 circle = 8 stitches).')
print(f'You have total of {total_stitches_before_bust} stitches at [Row {row_list_inc[-1]}].')
print('____________________________________________________\n____________________________________________________')
print('Disconnecting arms from bust:\n________________________________________________________')
print(
    f'[Row {row_list_inc[-1] + 1}]: Knit until Marker-1, set main yarn aside.\nClose {sleeve_disconnected} stitches of the arm using differen yarn color(including {int(reglan / 2)} reglan stitches at the beginning and end of the sleeve).\nReturn to main yarn.\nTurn it around the needle loosely to make loops for future 8 stitches.\nKnit back part until Marker-3, set main yarn aside.\nClose {sleeve_disconnected} stitches of the arm using different yarn color(including {int(reglan / 2)} reglan stitches at the beginning and end of the sleeve).\nReturn to main yarn.\nTurn it around the needle loosely to make loops for future 8 stitches.\nKnit until the final Marker.')
print('________________________________________________________')
print(f'You have total of {total_stitches_bust} stitches at [Row {first_row_bust}].')
print(
    '________________________________________________________\n________________________________________________________')
print('Working down from the bust:\n________________________________________________________')
print(
    f'[Row {first_row_bust + 1}]: Knit in the circle, knit 8 stitches under armpit from the yarn, that you turned around the needle in previous row, continue knitting and repeat under next armpit, knit until end of the row.')
print('________________________________________________________')
print(
    f'Knit bust part in the circle without increases until [Row {rows_until_bottom}].\nYou can make last 4-8 rows ribbed with 1x1 rib or 2x2 rib.')
print(
    '________________________________________________________\n________________________________________________________')
print('Working down the sleeve (repeat for each sleeve):\n________________________________________________________')
print(
    f'Knit the sleeve in the circle until [Row {row_list_dec[-1]}] (included) and decrease 1 stich around every reglan line in Row: {decrease_row_number}, (total decrease in 1 circle = 2 stitches).')
print(
    f'You have total of {total_stitches_wrist} stitches at [Row {row_list_dec[-1]}].\nYou can make last 4-8 rows ribbed with 1x1 rib or 2x2 rib.')
