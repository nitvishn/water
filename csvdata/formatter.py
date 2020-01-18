latitudes = [12.956571, 12.963335, 12.964726, 12.960354, 12.960891, 12.964705, 12.958302, 12.965713, 12.959234, 12.959488, 12.957077, 12.963285, 12.964909, 12.959709, 12.959524, 12.963802, 12.957282, 12.957316, 12.959618, 12.960027, 12.959331, 12.958868, 12.96019, 12.963076, 12.960105, 12.957874, 12.962297, 12.961354, 12.963367, 12.966161, 12.964703, 12.965052, 12.964377, 12.966297, 12.959137, 12.96059, 12.957545, 12.962938, 12.96064, 12.957006, 12.963911, 12.959575, 12.956927, 12.9642, 12.964204, 12.956118, 12.961538, 12.962497, 12.964919, 12.963858, 12.973602, 12.981799, 12.975025, 12.969996, 12.975174, 12.980189, 12.970323, 12.982653, 12.97809, 12.978109, 12.978542, 12.972658, 12.973206, 12.968921, 12.967528, 12.973443, 12.976199, 12.967706, 12.980708, 12.970029, 12.974437, 12.977815, 12.969371, 12.980536, 12.981002, 12.978102, 12.973927, 12.979846, 12.979389, 12.977682, 12.967307, 12.967528, 12.968571, 12.969226, 12.978053, 12.977543, 12.977727, 12.982015, 12.971832, 12.969732, 12.972259, 12.979543, 12.969602, 12.975937, 12.971431, 12.973726, 12.968375, 12.971642, 12.97697]
longitudes = [77.729298, 77.731373, 77.730913, 77.72896, 77.729717, 77.732385, 77.731536, 77.733001, 77.731708, 77.730398, 77.730537, 77.730046, 77.73185, 77.732757, 77.729938, 77.7294, 77.731624, 77.729006, 77.728992, 77.731277, 77.730066, 77.729779, 77.729578, 77.729724, 77.72915, 77.731881, 77.728932, 77.732766, 77.728888, 77.728843, 77.730871, 77.731476, 77.731625, 77.737913, 77.747127, 77.734745, 77.739165, 77.749554, 77.746063, 77.737988, 77.73564, 77.747341, 77.738642, 77.747903, 77.747396, 77.734348, 77.744204, 77.735256, 77.733443, 77.741126, 77.749067, 77.735578, 77.738979, 77.739396, 77.741607, 77.748973, 77.740496, 77.737822, 77.7427, 77.73362, 77.74378, 77.746257, 77.747544, 77.746222, 77.743518, 77.736354, 77.753839, 77.754576, 77.751745, 77.751978, 77.756438, 77.752657, 77.75358, 77.750793, 77.75291, 77.754129, 77.750508, 77.750328, 77.753755, 77.754817, 77.754235, 77.756119, 77.755892, 77.752042, 77.753332, 77.752487, 77.757788, 77.757254, 77.75649, 77.750659, 77.753974, 77.755416, 77.75646, 77.757267, 77.755027, 77.755326, 77.757072, 77.753862, 77.751232]
infile = open('moreCommunities.csv', 'r')
outfile = open('communitiesData.csv', 'w')
file_data = [s.rstrip('\n') for s in infile.readlines()]

for i in range(len(file_data) - 1):
  outfile.write(file_data[i] + "," + "1" + '\n')

outfile.close() 