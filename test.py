def parse_segment(segment):
    #Get the header
    split_segment = segment.split("|||")
    header = split_segment[0:3]
    #Get the sequence number
    seq = split_segment[3]
    #Get the data
    data = split_segment[4]
    #Return the data structure
    return header, seq, data


#Give me an example of the previous function in action
#Create a segment with SYN and SEQ headers
segment = "1|||0|||0|||001|||Hello"
#Parse the segment
header, seq, data = parse_segment(segment)
#Print the results
print("Header: " + str(header))
print("Sequence number: " + str(seq))
print("Data: " + str(data))
