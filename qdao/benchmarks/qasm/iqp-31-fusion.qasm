OPENQASM 2.0;
include "qelib1.inc";
qreg q[31];
h q[0];
h q[1];
cp(-339*pi) q[0],q[1];
h q[2];
cp(677.01322) q[0],q[2];
cp(-54.977871) q[1],q[2];
h q[3];
cp(-922.05744) q[1],q[3];
cp(1578.6503) q[2],q[3];
h q[4];
cp(-482.23447) q[3],q[4];
h q[5];
cp(183*pi) q[0],q[5];
cp(-711.57074) q[2],q[5];
cp(526.21677) q[3],q[5];
h q[6];
cp(-453*pi) q[1],q[6];
cp(1138.8273) q[2],q[6];
cp(1371.3052) q[3],q[6];
cp(-422.54421) q[5],q[6];
h q[7];
cp(-1292.7654) q[0],q[7];
cp(-136.65928) q[1],q[7];
cp(-239*pi) q[2],q[7];
cp(-771.261) q[3],q[7];
cp(526.21677) q[4],q[7];
cp(-325*pi) q[5],q[7];
cp(-1041.438) q[6],q[7];
h q[8];
cp(32.986723) q[0],q[8];
cp(381*pi) q[1],q[8];
cp(529.35836) q[2],q[8];
cp(-799.53533) q[4],q[8];
cp(934.62381) q[6],q[8];
cp(425*pi) q[7],q[8];
h q[9];
cp(-444.53536) q[0],q[9];
cp(218.34069) q[1],q[9];
cp(243*pi) q[3],q[9];
cp(513.6504) q[4],q[9];
cp(65*pi) q[5],q[9];
cp(-237*pi) q[6],q[9];
cp(-1443.5618) q[7],q[9];
h q[10];
cp(-369*pi) q[0],q[10];
cp(1368.1636) q[1],q[10];
cp(1207.9424) q[2],q[10];
cp(-1518.96) q[3],q[10];
cp(289*pi) q[5],q[10];
cp(7*pi) q[6],q[10];
cp(686.43799) q[7],q[10];
cp(1528.3848) q[8],q[10];
cp(-51.836279) q[9],q[10];
h q[11];
cp(413*pi) q[0],q[11];
cp(-1145.1105) q[1],q[11];
cp(-1305.3317) q[3],q[11];
cp(-31*pi) q[4],q[11];
cp(55*pi) q[7],q[11];
cp(-164.93361) q[8],q[11];
cp(-808.96011) q[9],q[11];
cp(1361.8804) q[10],q[11];
h q[12];
cp(865.50878) q[0],q[12];
cp(1113.6946) q[2],q[12];
cp(-227.76547) q[3],q[12];
cp(-1581.7919) q[4],q[12];
cp(115*pi) q[5],q[12];
cp(315*pi) q[6],q[12];
cp(467*pi) q[8],q[12];
cp(-714.71233) q[9],q[12];
cp(1434.137) q[10],q[12];
cp(-1588.0751) q[11],q[12];
h q[13];
cp(351*pi) q[0],q[13];
cp(-259*pi) q[1],q[13];
cp(-362.85395) q[3],q[13];
cp(63*pi) q[4],q[13];
cp(-271.74776) q[5],q[13];
cp(-423*pi) q[6],q[13];
cp(438.25218) q[7],q[13];
cp(834.09285) q[8],q[13];
cp(83*pi) q[9],q[13];
cp(1116.8362) q[10],q[13];
cp(-247*pi) q[11],q[13];
cp(-70.685835) q[12],q[13];
h q[14];
cp(755.55303) q[0],q[14];
cp(47*pi) q[2],q[14];
cp(-589.04862) q[5],q[14];
cp(915.77426) q[7],q[14];
cp(373*pi) q[8],q[14];
cp(824.66807) q[9],q[14];
cp(-423*pi) q[10],q[14];
cp(391.12829) q[12],q[14];
h q[15];
cp(896.9247) q[1],q[15];
cp(-251*pi) q[2],q[15];
cp(1116.8362) q[3],q[15];
cp(-290.59732) q[4],q[15];
cp(-1446.7034) q[5],q[15];
cp(-235*pi) q[6],q[15];
cp(-15*pi) q[7],q[15];
cp(73.827427) q[9],q[15];
cp(-209*pi) q[10],q[15];
cp(59*pi) q[11],q[15];
cp(-111.52654) q[12],q[15];
cp(-202.63273) q[13],q[15];
h q[16];
cp(-790.11055) q[0],q[16];
cp(1471.8362) q[2],q[16];
cp(680.15481) q[3],q[16];
cp(1490.6857) q[4],q[16];
cp(-1192.2344) q[5],q[16];
cp(-799.53533) q[6],q[16];
cp(764.97781) q[7],q[16];
cp(-54.977871) q[9],q[16];
cp(505*pi) q[12],q[16];
cp(959.75656) q[13],q[16];
cp(437*pi) q[14],q[16];
cp(145*pi) q[15],q[16];
h q[17];
cp(-1082.2787) q[0],q[17];
cp(-1518.96) q[1],q[17];
cp(-1578.6503) q[2],q[17];
cp(585.90703) q[3],q[17];
cp(1566.0839) q[4],q[17];
cp(234.04865) q[6],q[17];
cp(570.19907) q[7],q[17];
cp(344.0044) q[8],q[17];
cp(752.41144) q[10],q[17];
cp(915.77426) q[11],q[17];
cp(-323*pi) q[12],q[17];
cp(-611.03977) q[13],q[17];
cp(-1540.9512) q[14],q[17];
cp(1025.73) q[15],q[17];
cp(871.79196) q[16],q[17];
h q[18];
cp(1531.5264) q[0],q[18];
cp(-545.06633) q[1],q[18];
cp(-43*pi) q[2],q[18];
cp(265*pi) q[3],q[18];
cp(1540.9512) q[4],q[18];
cp(849.80081) q[5],q[18];
cp(-1214.2256) q[7],q[18];
cp(-509*pi) q[8],q[18];
cp(-862.36718) q[9],q[18];
cp(-143*pi) q[10],q[18];
cp(-45.553093) q[11],q[18];
cp(-381.70351) q[12],q[18];
cp(-491.65925) q[13],q[18];
cp(107*pi) q[15],q[18];
cp(1330.4645) q[16],q[18];
cp(-3*pi) q[17],q[18];
h q[19];
cp(708.42914) q[1],q[19];
cp(45*pi) q[3],q[19];
cp(-472.80969) q[4],q[19];
cp(215*pi) q[5],q[19];
cp(-821.52648) q[6],q[19];
cp(117*pi) q[7],q[19];
cp(-786.96896) q[8],q[19];
cp(-1069.7123) q[9],q[19];
cp(-307*pi) q[11],q[19];
cp(-37*pi) q[12],q[19];
cp(-53*pi) q[13],q[19];
cp(-972.32293) q[14],q[19];
cp(-13*pi) q[15],q[19];
cp(-780.68577) q[16],q[19];
cp(519.93358) q[17],q[19];
cp(-1072.8539) q[18],q[19];
h q[20];
cp(-1229.9335) q[0],q[20];
cp(-95.818576) q[1],q[20];
cp(1575.5087) q[2],q[20];
cp(-285*pi) q[3],q[20];
cp(-808.96011) q[4],q[20];
cp(1383.8716) q[5],q[20];
cp(1578.6503) q[7],q[20];
cp(-64.402649) q[9],q[20];
cp(1135.6857) q[10],q[20];
cp(-981.7477) q[11],q[20];
cp(301*pi) q[13],q[20];
cp(375*pi) q[14],q[20];
cp(13*pi) q[15],q[20];
cp(1355.5972) q[17],q[20];
cp(-86.393798) q[18],q[20];
cp(-1308.4733) q[19],q[20];
h q[21];
cp(-431*pi) q[0],q[21];
cp(-145*pi) q[1],q[21];
cp(774.40259) q[3],q[21];
cp(483*pi) q[4],q[21];
cp(724.13711) q[6],q[21];
cp(407*pi) q[8],q[21];
cp(-871.79196) q[9],q[21];
cp(1050.8627) q[10],q[21];
cp(-158.65043) q[11],q[21];
cp(203*pi) q[12],q[21];
cp(944.04859) q[14],q[21];
cp(-487*pi) q[15],q[21];
cp(-369.13714) q[17],q[21];
cp(-1041.438) q[18],q[21];
cp(-281*pi) q[20],q[21];
h q[22];
cp(-604.75659) q[0],q[22];
cp(481*pi) q[1],q[22];
cp(-449*pi) q[2],q[22];
cp(-203*pi) q[4],q[22];
cp(761.83622) q[5],q[22];
cp(-391.12829) q[6],q[22];
cp(1446.7034) q[7],q[22];
cp(1016.3052) q[8],q[22];
cp(-950.33178) q[9],q[22];
cp(499*pi) q[10],q[22];
cp(-117*pi) q[11],q[22];
cp(-405*pi) q[12],q[22];
cp(-207*pi) q[13],q[22];
cp(349*pi) q[14],q[22];
cp(-297*pi) q[15],q[22];
cp(1321.0397) q[17],q[22];
cp(1449.845) q[18],q[22];
cp(64.402649) q[21],q[22];
h q[23];
cp(739.84507) q[1],q[23];
cp(-251*pi) q[3],q[23];
cp(1405.8627) q[4],q[23];
cp(141*pi) q[6],q[23];
cp(1380.73) q[7],q[23];
cp(-221.48228) q[8],q[23];
cp(389*pi) q[9],q[23];
cp(1434.137) q[11],q[23];
cp(1584.9335) q[12],q[23];
cp(-367*pi) q[13],q[23];
cp(1387.0132) q[14],q[23];
cp(-89.535391) q[15],q[23];
cp(-1569.2255) q[18],q[23];
cp(604.75659) q[19],q[23];
cp(337.72121) q[22],q[23];
h q[24];
cp(-821.52648) q[0],q[24];
cp(-383*pi) q[2],q[24];
cp(-944.04859) q[4],q[24];
cp(-1251.9247) q[5],q[24];
cp(-421*pi) q[6],q[24];
cp(378.56191) q[7],q[24];
cp(1082.2787) q[8],q[24];
cp(-1000.5973) q[9],q[24];
cp(-1010.022) q[10],q[24];
cp(994.31407) q[11],q[24];
cp(-347*pi) q[12],q[24];
cp(742.98666) q[13],q[24];
cp(145*pi) q[14],q[24];
cp(1226.7919) q[15],q[24];
cp(1267.6326) q[16],q[24];
cp(-171.2168) q[17],q[24];
cp(-1393.2963) q[19],q[24];
cp(379*pi) q[20],q[24];
cp(-51*pi) q[21],q[24];
cp(1465.553) q[22],q[24];
h q[25];
cp(780.68577) q[1],q[25];
cp(-495*pi) q[3],q[25];
cp(1396.4379) q[4],q[25];
cp(-1079.1371) q[5],q[25];
cp(799.53533) q[8],q[25];
cp(1185.9512) q[10],q[25];
cp(-1553.5176) q[11],q[25];
cp(219*pi) q[14],q[25];
cp(157*pi) q[15],q[25];
cp(-896.9247) q[16],q[25];
cp(1141.9689) q[17],q[25];
cp(1421.5707) q[18],q[25];
cp(695.86277) q[19],q[25];
cp(658.16366) q[20],q[25];
cp(1452.9866) q[21],q[25];
cp(758.69463) q[22],q[25];
cp(-39.269908) q[23],q[25];
cp(-63*pi) q[24],q[25];
h q[26];
cp(-903.20789) q[0],q[26];
cp(303*pi) q[2],q[26];
cp(-1465.553) q[5],q[26];
cp(1349.314) q[6],q[26];
cp(-969.18133) q[7],q[26];
cp(-1544.0928) q[9],q[26];
cp(-1050.8627) q[10],q[26];
cp(-1330.4645) q[12],q[26];
cp(11*pi/2) q[13],q[26];
cp(-337*pi) q[14],q[26];
cp(878.07515) q[15],q[26];
cp(-419.40262) q[16],q[26];
cp(708.42914) q[17],q[26];
cp(-516.79199) q[19],q[26];
cp(-1261.3495) q[20],q[26];
cp(-1512.6769) q[21],q[26];
cp(-127*pi) q[22],q[26];
cp(-1261.3495) q[23],q[26];
cp(-626.74773) q[24],q[26];
cp(11*pi/2) q[25],q[26];
h q[27];
cp(-1113.6946) q[0],q[27];
cp(1493.8273) q[1],q[27];
cp(127*pi) q[2],q[27];
cp(-193*pi) q[3],q[27];
cp(-1082.2787) q[5],q[27];
cp(246.61502) q[6],q[27];
cp(-317*pi) q[7],q[27];
cp(-1201.6592) q[8],q[27];
cp(-1355.5972) q[9],q[27];
cp(573.34066) q[10],q[27];
cp(331.43802) q[11],q[27];
cp(-1317.8981) q[12],q[27];
cp(-47*pi) q[13],q[27];
cp(-1380.73) q[14],q[27];
cp(-355*pi) q[15],q[27];
cp(-284.31414) q[16],q[27];
cp(-1427.8539) q[17],q[27];
cp(-pi) q[18],q[27];
cp(87*pi) q[19],q[27];
cp(230.90706) q[20],q[27];
cp(-73.827427) q[21],q[27];
cp(-347.14599) q[25],q[27];
cp(545.06633) q[26],q[27];
h q[28];
cp(1317.8981) q[0],q[28];
cp(-925.19904) q[1],q[28];
p(-157.86503) q[1];
h q[1];
cp(840.37603) q[2],q[28];
cp(-1317.8981) q[3],q[28];
cp(-730.42029) q[4],q[28];
cp(-1154.5353) q[5],q[28];
cp(-343*pi) q[6],q[28];
cp(3*pi/2) q[7],q[28];
cp(878.07515) q[8],q[28];
cp(-563.91588) q[9],q[28];
cp(-193.20795) q[10],q[28];
cp(-111*pi) q[11],q[28];
p(-45.945793) q[11];
h q[11];
cp(1286.4822) q[12],q[28];
cp(-281*pi) q[15],q[28];
cp(-796.39374) q[16],q[28];
cp(-97*pi) q[17],q[28];
cp(815.24329) q[18],q[28];
cp(335*pi) q[21],q[28];
cp(944.04859) q[22],q[28];
cp(501.08403) q[23],q[28];
cp(-497*pi) q[24],q[28];
cp(1343.0309) q[25],q[28];
cp(-1396.4379) q[26],q[28];
h q[29];
cp(-1540.9512) q[0],q[29];
cp(-1129.4026) q[3],q[29];
cp(-165*pi) q[5],q[29];
p(-60.082959) q[5];
h q[5];
cp(-123*pi) q[6],q[29];
cp(-1421.5707) q[7],q[29];
cp(-457*pi) q[8],q[29];
cp(1471.8362) q[9],q[29];
cp(790.11055) q[10],q[29];
cp(45*pi) q[12],q[29];
p(299.6294) q[12];
h q[12];
cp(-915.77426) q[14],q[29];
cp(959.75656) q[15],q[29];
h q[15];
cp(560.77429) q[18],q[29];
cp(-11*pi/2) q[19],q[29];
cp(303.16369) q[20],q[29];
p(-328.29643) q[20];
h q[20];
cp(-267*pi) q[21],q[29];
cp(143*pi) q[22],q[29];
cp(-202.63273) q[24],q[29];
p(-232.87056) q[24];
h q[24];
cp(538.78314) q[25],q[29];
h q[25];
cp(-77*pi) q[28],q[29];
p(202.63273) q[28];
h q[28];
h q[30];
cp(-1459.2698) q[0],q[30];
p(347.53869) q[0];
h q[0];
cp(-411*pi) q[2],q[30];
p(-243.47343) q[2];
h q[2];
cp(-1396.4379) q[3],q[30];
p(300.8075) q[3];
h q[3];
cp(437*pi) q[4],q[30];
p(267.82077) q[4];
h q[4];
cp(243.47343) q[6],q[30];
p(-159.82853) q[6];
h q[6];
cp(9*pi/2) q[7],q[30];
p(-307.09068) q[7];
h q[7];
cp(23*pi) q[8],q[30];
p(-374.63492) q[8];
h q[8];
cp(243.47343) q[9],q[30];
cp(-391*pi) q[10],q[30];
p(124.48561) q[10];
h q[10];
cp(417*pi) q[13],q[30];
p(269.78427) q[13];
h q[13];
cp(-585.90703) q[14],q[30];
p(288.63383) q[14];
h q[14];
cp(-59*pi) q[16],q[30];
p(62.046455) q[16];
h q[16];
cp(1145.1105) q[17],q[30];
p(-186.53206) q[17];
h q[17];
cp(397.41147) q[18],q[30];
p(-212.0575) q[18];
h q[18];
cp(215.1991) q[19],q[30];
h q[19];
cp(1365.022) q[21],q[30];
p(-322.40595) q[21];
h q[21];
cp(321*pi) q[22],q[30];
p(-165.71901) q[22];
h q[22];
cp(-142.94247) q[23],q[30];
p(-121.34402) q[23];
h q[23];
cp(724.13711) q[26],q[30];
p(100.92366) q[26];
h q[26];
cp(1016.3052) q[27],q[30];
p(327.51103) q[27];
h q[27];
cp(-1151.3937) q[29],q[30];
p(-338.89931) q[29];
h q[29];
p(397.80417) q[30];
h q[30];
p(-57.726765) q[9];
h q[9];
