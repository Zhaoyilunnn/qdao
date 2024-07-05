OPENQASM 2.0;
include "qelib1.inc";
gate cs q0,q1 { p(pi/4) q0; cx q0,q1; p(-pi/4) q1; cx q0,q1; p(pi/4) q1; }
gate r(param0,param1) q0 { u3(param0,param1 - pi/2,pi/2 - 1.0*param1) q0; }
gate rzx(param0) q0,q1 { h q1; cx q0,q1; rz(param0) q1; cx q0,q1; h q1; }
gate ecr q0,q1 { rzx(pi/4) q0,q1; x q0; rzx(-pi/4) q0,q1; }
gate xx_plus_yy(param0,param1) q0,q1 { rz(param1) q0; rz(-pi/2) q1; sx q1; rz(pi/2) q1; s q0; cx q1,q0; ry(-0.5*param0) q1; ry(-0.5*param0) q0; cx q1,q0; sdg q0; rz(-pi/2) q1; sxdg q1; rz(pi/2) q1; rz(-1.0*param1) q0; }
qreg q[6];
cs q[3],q[1];
h q[2];
u1(4.022094993754273) q[5];
u3(6.084784558857044,4.904826475850047,2.092830736530902) q[0];
id q[4];
cu3(4.232797655148895,5.178361123615903,5.788390605570175) q[1],q[4];
id q[3];
rxx(3.4744789232730504) q[5],q[2];
h q[0];
r(2.2802981344683273,2.2242333037792226) q[4];
r(2.4984515523171806,4.461253902474105) q[2];
u2(1.7421143821650211,6.069529643610582) q[0];
id q[3];
rx(0.25108393389389366) q[5];
h q[1];
rzx(4.174861982785091) q[2],q[0];
sxdg q[4];
ecr q[1],q[3];
u1(0.4695270736633402) q[5];
rx(6.098341395819053) q[2];
r(3.452055646916473,3.5577139566954608) q[4];
cu3(5.709147715274552,1.692769900921249,1.114380070599721) q[0],q[3];
rz(0.2653533041134066) q[5];
s q[1];
cs q[1],q[0];
z q[5];
cu(2.2558859258589745,3.928114657830361,1.3661512899781587,5.259189475300748) q[4],q[3];
x q[2];
rz(1.7876191946647977) q[5];
cz q[3],q[4];
swap q[2],q[0];
rx(0.32580489855587447) q[1];
cs q[5],q[1];
rzx(1.614638034109668) q[4],q[0];
ecr q[3],q[2];
swap q[4],q[2];
rz(5.681118457387238) q[0];
r(2.4740871856295996,2.6672360156570445) q[5];
crz(0.7130352940087009) q[1],q[3];
crx(0.35209547832369187) q[3],q[5];
u3(6.103914699537293,3.778384194124074,3.4016930835803363) q[4];
t q[1];
xx_plus_yy(3.8853738638383186,0.597760686647738) q[2],q[0];