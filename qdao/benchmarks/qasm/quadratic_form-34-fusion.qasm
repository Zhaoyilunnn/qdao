OPENQASM 2.0;
include "qelib1.inc";
qreg q0[3];
qreg q1[31];
p(pi/2147483648) q0[0];
p(pi/2147483648) q0[1];
p(pi/2147483648) q0[2];
u2(0,pi) q1[0];
u2(0,pi) q1[1];
u2(0,pi) q1[2];
u2(0,pi) q1[3];
u2(0,pi) q1[4];
u2(0,pi) q1[5];
u2(0,pi) q1[6];
u2(0,pi) q1[7];
u2(0,pi) q1[8];
u2(0,pi) q1[9];
u2(0,pi) q1[10];
u2(0,pi) q1[11];
u2(0,pi) q1[12];
u2(0,pi) q1[13];
u2(0,pi) q1[14];
u2(0,pi) q1[15];
u2(0,pi) q1[16];
u2(0,pi) q1[17];
u2(0,pi) q1[18];
u2(0,pi) q1[19];
u2(0,pi) q1[20];
u2(0,pi) q1[21];
u2(0,pi) q1[22];
u2(0,pi) q1[23];
u2(0,pi) q1[24];
u2(0,pi) q1[25];
u2(0,pi) q1[26];
u2(0,pi) q1[27];
u2(0,pi) q1[28];
u2(0,pi) q1[29];
u2(0,pi) q1[30];
cx q0[0],q1[30];
p(-pi/2147483648) q1[30];
cx q0[0],q1[30];
p(pi/1073741824) q0[0];
cx q0[0],q1[29];
p(-pi/1073741824) q1[29];
cx q0[0],q1[29];
p(pi/536870912) q0[0];
cx q0[0],q1[28];
p(-pi/536870912) q1[28];
cx q0[0],q1[28];
p(pi/268435456) q0[0];
cx q0[0],q1[27];
p(-pi/268435456) q1[27];
cx q0[0],q1[27];
p(pi/134217728) q0[0];
cx q0[0],q1[26];
p(-pi/134217728) q1[26];
cx q0[0],q1[26];
p(pi/67108864) q0[0];
cx q0[0],q1[25];
p(-pi/67108864) q1[25];
cx q0[0],q1[25];
p(pi/33554432) q0[0];
cx q0[0],q1[24];
p(-pi/33554432) q1[24];
cx q0[0],q1[24];
p(pi/16777216) q0[0];
cx q0[0],q1[23];
p(-pi/16777216) q1[23];
cx q0[0],q1[23];
p(pi/8388608) q0[0];
cx q0[0],q1[22];
p(-pi/8388608) q1[22];
cx q0[0],q1[22];
p(pi/4194304) q0[0];
cx q0[0],q1[21];
p(-pi/4194304) q1[21];
cx q0[0],q1[21];
p(pi/2097152) q0[0];
cx q0[0],q1[20];
p(-pi/2097152) q1[20];
cx q0[0],q1[20];
p(pi/1048576) q0[0];
cx q0[0],q1[19];
p(-pi/1048576) q1[19];
cx q0[0],q1[19];
p(pi/524288) q0[0];
cx q0[0],q1[18];
p(-pi/524288) q1[18];
cx q0[0],q1[18];
p(pi/262144) q0[0];
cx q0[0],q1[17];
p(-pi/262144) q1[17];
cx q0[0],q1[17];
p(pi/131072) q0[0];
cx q0[0],q1[16];
p(-pi/131072) q1[16];
cx q0[0],q1[16];
p(pi/65536) q0[0];
cx q0[0],q1[15];
p(-pi/65536) q1[15];
cx q0[0],q1[15];
p(pi/32768) q0[0];
cx q0[0],q1[14];
p(-pi/32768) q1[14];
cx q0[0],q1[14];
p(pi/16384) q0[0];
cx q0[0],q1[13];
p(-pi/16384) q1[13];
cx q0[0],q1[13];
p(pi/8192) q0[0];
cx q0[0],q1[12];
p(-pi/8192) q1[12];
cx q0[0],q1[12];
p(pi/4096) q0[0];
cx q0[0],q1[11];
p(-pi/4096) q1[11];
cx q0[0],q1[11];
p(pi/2048) q0[0];
cx q0[0],q1[10];
p(-pi/2048) q1[10];
cx q0[0],q1[10];
p(pi/1024) q0[0];
cx q0[0],q1[9];
p(pi/2048) q1[10];
p(pi/4096) q1[11];
p(pi/8192) q1[12];
p(pi/16384) q1[13];
p(pi/32768) q1[14];
p(pi/65536) q1[15];
p(pi/131072) q1[16];
p(pi/262144) q1[17];
p(pi/524288) q1[18];
p(pi/1048576) q1[19];
p(pi/2097152) q1[20];
p(pi/4194304) q1[21];
p(pi/8388608) q1[22];
p(pi/16777216) q1[23];
p(pi/33554432) q1[24];
p(pi/67108864) q1[25];
p(pi/134217728) q1[26];
p(pi/268435456) q1[27];
p(pi/536870912) q1[28];
p(pi/1073741824) q1[29];
p(pi/2147483648) q1[30];
cx q0[1],q1[30];
p(-pi/2147483648) q1[30];
cx q0[1],q1[30];
p(pi/1073741824) q0[1];
cx q0[1],q1[29];
p(-pi/1073741824) q1[29];
cx q0[1],q1[29];
p(pi/536870912) q0[1];
cx q0[1],q1[28];
p(-pi/536870912) q1[28];
cx q0[1],q1[28];
p(pi/268435456) q0[1];
cx q0[1],q1[27];
p(-pi/268435456) q1[27];
cx q0[1],q1[27];
p(pi/134217728) q0[1];
cx q0[1],q1[26];
p(-pi/134217728) q1[26];
cx q0[1],q1[26];
p(pi/67108864) q0[1];
cx q0[1],q1[25];
p(-pi/67108864) q1[25];
cx q0[1],q1[25];
p(pi/33554432) q0[1];
cx q0[1],q1[24];
p(-pi/33554432) q1[24];
cx q0[1],q1[24];
p(pi/16777216) q0[1];
cx q0[1],q1[23];
p(-pi/16777216) q1[23];
cx q0[1],q1[23];
p(pi/8388608) q0[1];
cx q0[1],q1[22];
p(-pi/8388608) q1[22];
cx q0[1],q1[22];
p(pi/4194304) q0[1];
cx q0[1],q1[21];
p(-pi/4194304) q1[21];
cx q0[1],q1[21];
p(pi/2097152) q0[1];
cx q0[1],q1[20];
p(-pi/2097152) q1[20];
cx q0[1],q1[20];
p(pi/1048576) q0[1];
cx q0[1],q1[19];
p(-pi/1048576) q1[19];
cx q0[1],q1[19];
p(pi/524288) q0[1];
cx q0[1],q1[18];
p(-pi/524288) q1[18];
cx q0[1],q1[18];
p(pi/262144) q0[1];
cx q0[1],q1[17];
p(-pi/262144) q1[17];
cx q0[1],q1[17];
p(pi/131072) q0[1];
cx q0[1],q1[16];
p(-pi/131072) q1[16];
cx q0[1],q1[16];
p(pi/65536) q0[1];
cx q0[1],q1[15];
p(-pi/65536) q1[15];
cx q0[1],q1[15];
p(pi/32768) q0[1];
cx q0[1],q1[14];
p(-pi/32768) q1[14];
cx q0[1],q1[14];
p(pi/16384) q0[1];
cx q0[1],q1[13];
p(-pi/16384) q1[13];
cx q0[1],q1[13];
p(pi/8192) q0[1];
cx q0[1],q1[12];
p(-pi/8192) q1[12];
cx q0[1],q1[12];
p(pi/4096) q0[1];
cx q0[1],q1[11];
p(-pi/4096) q1[11];
cx q0[1],q1[11];
p(pi/2048) q0[1];
cx q0[1],q1[10];
p(-pi/2048) q1[10];
cx q0[1],q1[10];
p(pi/1024) q0[1];
p(pi/2048) q1[10];
p(pi/4096) q1[11];
p(pi/8192) q1[12];
p(pi/16384) q1[13];
p(pi/32768) q1[14];
p(pi/65536) q1[15];
p(pi/131072) q1[16];
p(pi/262144) q1[17];
p(pi/524288) q1[18];
p(pi/1048576) q1[19];
p(pi/2097152) q1[20];
p(pi/4194304) q1[21];
p(pi/8388608) q1[22];
p(pi/16777216) q1[23];
p(pi/33554432) q1[24];
p(pi/67108864) q1[25];
p(pi/134217728) q1[26];
p(pi/268435456) q1[27];
p(pi/536870912) q1[28];
p(pi/1073741824) q1[29];
p(pi/2147483648) q1[30];
cx q0[2],q1[30];
p(-pi/2147483648) q1[30];
cx q0[2],q1[30];
p(pi/1073741824) q0[2];
cx q0[2],q1[29];
p(-pi/1073741824) q1[29];
cx q0[2],q1[29];
p(pi/536870912) q0[2];
cx q0[2],q1[28];
p(-pi/536870912) q1[28];
cx q0[2],q1[28];
p(pi/268435456) q0[2];
cx q0[2],q1[27];
p(-pi/268435456) q1[27];
cx q0[2],q1[27];
p(pi/134217728) q0[2];
cx q0[2],q1[26];
p(-pi/134217728) q1[26];
cx q0[2],q1[26];
p(pi/67108864) q0[2];
cx q0[2],q1[25];
p(-pi/67108864) q1[25];
cx q0[2],q1[25];
p(pi/33554432) q0[2];
cx q0[2],q1[24];
p(-pi/33554432) q1[24];
cx q0[2],q1[24];
p(pi/16777216) q0[2];
cx q0[2],q1[23];
p(-pi/16777216) q1[23];
cx q0[2],q1[23];
p(pi/8388608) q0[2];
cx q0[2],q1[22];
p(-pi/8388608) q1[22];
cx q0[2],q1[22];
p(pi/4194304) q0[2];
cx q0[2],q1[21];
p(-pi/4194304) q1[21];
cx q0[2],q1[21];
p(pi/2097152) q0[2];
cx q0[2],q1[20];
p(-pi/2097152) q1[20];
cx q0[2],q1[20];
p(pi/1048576) q0[2];
cx q0[2],q1[19];
p(-pi/1048576) q1[19];
cx q0[2],q1[19];
p(pi/524288) q0[2];
cx q0[2],q1[18];
p(-pi/524288) q1[18];
cx q0[2],q1[18];
p(pi/262144) q0[2];
cx q0[2],q1[17];
p(-pi/262144) q1[17];
cx q0[2],q1[17];
p(pi/131072) q0[2];
cx q0[2],q1[16];
p(-pi/131072) q1[16];
cx q0[2],q1[16];
p(pi/65536) q0[2];
cx q0[2],q1[15];
p(-pi/65536) q1[15];
cx q0[2],q1[15];
p(pi/32768) q0[2];
cx q0[2],q1[14];
p(-pi/32768) q1[14];
cx q0[2],q1[14];
p(pi/16384) q0[2];
cx q0[2],q1[13];
p(-pi/16384) q1[13];
cx q0[2],q1[13];
p(pi/8192) q0[2];
cx q0[2],q1[12];
p(-pi/8192) q1[12];
cx q0[2],q1[12];
p(pi/4096) q0[2];
cx q0[2],q1[11];
p(-pi/4096) q1[11];
cx q0[2],q1[11];
p(pi/2048) q0[2];
cx q0[2],q1[10];
p(-pi/2048) q1[10];
cx q0[2],q1[10];
p(pi/1024) q0[2];
p(pi/2048) q1[10];
p(pi/4096) q1[11];
p(pi/8192) q1[12];
p(pi/16384) q1[13];
p(pi/32768) q1[14];
p(pi/65536) q1[15];
p(pi/131072) q1[16];
p(pi/262144) q1[17];
p(pi/524288) q1[18];
p(pi/1048576) q1[19];
p(pi/2097152) q1[20];
p(pi/4194304) q1[21];
p(pi/8388608) q1[22];
p(pi/16777216) q1[23];
p(pi/33554432) q1[24];
p(pi/67108864) q1[25];
p(pi/134217728) q1[26];
p(pi/268435456) q1[27];
p(pi/536870912) q1[28];
p(pi/1073741824) q1[29];
p(pi/2147483648) q1[30];
p(-pi/1024) q1[9];
cx q0[0],q1[9];
p(pi/512) q0[0];
cx q0[0],q1[8];
p(-pi/512) q1[8];
cx q0[0],q1[8];
p(pi/256) q0[0];
cx q0[0],q1[7];
p(-pi/256) q1[7];
cx q0[0],q1[7];
p(pi/128) q0[0];
cx q0[0],q1[6];
p(-pi/128) q1[6];
cx q0[0],q1[6];
p(pi/64) q0[0];
cx q0[0],q1[5];
p(-pi/64) q1[5];
cx q0[0],q1[5];
p(pi/32) q0[0];
cx q0[0],q1[4];
p(-pi/32) q1[4];
cx q0[0],q1[4];
p(pi/16) q0[0];
cx q0[0],q1[3];
p(-pi/16) q1[3];
cx q0[0],q1[3];
p(pi/8) q0[0];
cx q0[0],q1[2];
p(-pi/8) q1[2];
cx q0[0],q1[2];
p(pi/4) q0[0];
cx q0[0],q1[1];
p(-pi/4) q1[1];
cx q0[0],q1[1];
p(pi/2) q0[0];
cx q0[0],q1[0];
p(-pi/2) q1[0];
cx q0[0],q1[0];
p(pi/2) q1[0];
p(pi/4) q1[1];
p(pi/8) q1[2];
p(pi/16) q1[3];
p(pi/32) q1[4];
p(pi/64) q1[5];
p(pi/128) q1[6];
p(pi/256) q1[7];
p(pi/512) q1[8];
p(pi/1024) q1[9];
cx q0[1],q1[9];
p(-pi/1024) q1[9];
cx q0[1],q1[9];
p(pi/512) q0[1];
cx q0[1],q1[8];
p(-pi/512) q1[8];
cx q0[1],q1[8];
p(pi/256) q0[1];
cx q0[1],q1[7];
p(-pi/256) q1[7];
cx q0[1],q1[7];
p(pi/128) q0[1];
cx q0[1],q1[6];
p(-pi/128) q1[6];
cx q0[1],q1[6];
p(pi/64) q0[1];
cx q0[1],q1[5];
p(-pi/64) q1[5];
cx q0[1],q1[5];
p(pi/32) q0[1];
cx q0[1],q1[4];
p(-pi/32) q1[4];
cx q0[1],q1[4];
p(pi/16) q0[1];
cx q0[1],q1[3];
p(-pi/16) q1[3];
cx q0[1],q1[3];
p(pi/8) q0[1];
cx q0[1],q1[2];
p(-pi/8) q1[2];
cx q0[1],q1[2];
p(pi/4) q0[1];
cx q0[1],q1[1];
p(-pi/4) q1[1];
cx q0[1],q1[1];
p(pi/2) q0[1];
cx q0[1],q1[0];
p(-pi/2) q1[0];
cx q0[1],q1[0];
p(pi/2) q1[0];
p(pi/4) q1[1];
p(pi/8) q1[2];
p(pi/16) q1[3];
p(pi/32) q1[4];
p(pi/64) q1[5];
p(pi/128) q1[6];
p(pi/256) q1[7];
p(pi/512) q1[8];
p(pi/1024) q1[9];
cx q0[2],q1[9];
p(-pi/1024) q1[9];
cx q0[2],q1[9];
p(pi/512) q0[2];
cx q0[2],q1[8];
p(-pi/512) q1[8];
cx q0[2],q1[8];
p(pi/256) q0[2];
cx q0[2],q1[7];
p(-pi/256) q1[7];
cx q0[2],q1[7];
p(pi/128) q0[2];
cx q0[2],q1[6];
p(-pi/128) q1[6];
cx q0[2],q1[6];
p(pi/64) q0[2];
cx q0[2],q1[5];
p(-pi/64) q1[5];
cx q0[2],q1[5];
p(pi/32) q0[2];
cx q0[2],q1[4];
p(-pi/32) q1[4];
cx q0[2],q1[4];
p(pi/16) q0[2];
cx q0[2],q1[3];
p(-pi/16) q1[3];
cx q0[2],q1[3];
p(pi/8) q0[2];
cx q0[2],q1[2];
p(-pi/8) q1[2];
cx q0[2],q1[2];
p(pi/4) q0[2];
cx q0[2],q1[1];
p(-pi/4) q1[1];
cx q0[2],q1[1];
p(pi/2) q0[2];
cx q0[2],q1[0];
p(-pi/2) q1[0];
cx q0[2],q1[0];
p(pi/2) q1[0];
h q1[0];
p(pi/4) q1[1];
cp(-pi/2) q1[1],q1[0];
h q1[1];
p(pi/8) q1[2];
cp(-pi/4) q1[2],q1[0];
cp(-pi/2) q1[2],q1[1];
h q1[2];
p(pi/16) q1[3];
cp(-pi/8) q1[3],q1[0];
cp(-pi/4) q1[3],q1[1];
cp(-pi/2) q1[3],q1[2];
h q1[3];
p(pi/32) q1[4];
cp(-pi/16) q1[4],q1[0];
cp(-pi/8) q1[4],q1[1];
cp(-pi/4) q1[4],q1[2];
cp(-pi/2) q1[4],q1[3];
h q1[4];
p(pi/64) q1[5];
cp(-pi/32) q1[5],q1[0];
cp(-pi/16) q1[5],q1[1];
cp(-pi/8) q1[5],q1[2];
cp(-pi/4) q1[5],q1[3];
cp(-pi/2) q1[5],q1[4];
h q1[5];
p(pi/128) q1[6];
cp(-pi/64) q1[6],q1[0];
cp(-pi/32) q1[6],q1[1];
cp(-pi/16) q1[6],q1[2];
cp(-pi/8) q1[6],q1[3];
cp(-pi/4) q1[6],q1[4];
cp(-pi/2) q1[6],q1[5];
h q1[6];
p(pi/256) q1[7];
cp(-pi/128) q1[7],q1[0];
cp(-pi/64) q1[7],q1[1];
cp(-pi/32) q1[7],q1[2];
cp(-pi/16) q1[7],q1[3];
cp(-pi/8) q1[7],q1[4];
cp(-pi/4) q1[7],q1[5];
cp(-pi/2) q1[7],q1[6];
h q1[7];
p(pi/512) q1[8];
cp(-pi/256) q1[8],q1[0];
cp(-pi/128) q1[8],q1[1];
cp(-pi/64) q1[8],q1[2];
cp(-pi/32) q1[8],q1[3];
cp(-pi/16) q1[8],q1[4];
cp(-pi/8) q1[8],q1[5];
cp(-pi/4) q1[8],q1[6];
cp(-pi/2) q1[8],q1[7];
h q1[8];
p(pi/1024) q1[9];
cp(-pi/512) q1[9],q1[0];
cp(-pi/1024) q1[10],q1[0];
cp(-pi/2048) q1[11],q1[0];
cp(-pi/4096) q1[12],q1[0];
cp(-pi/8192) q1[13],q1[0];
cp(-pi/16384) q1[14],q1[0];
cp(-pi/32768) q1[15],q1[0];
cp(-pi/65536) q1[16],q1[0];
cp(-pi/131072) q1[17],q1[0];
cp(-pi/262144) q1[18],q1[0];
cp(-pi/524288) q1[19],q1[0];
cp(-pi/1048576) q1[20],q1[0];
cp(-pi/2097152) q1[21],q1[0];
cp(-pi/4194304) q1[22],q1[0];
cp(-pi/8388608) q1[23],q1[0];
cp(-pi/16777216) q1[24],q1[0];
cp(-pi/33554432) q1[25],q1[0];
cp(-pi/67108864) q1[26],q1[0];
cp(-pi/134217728) q1[27],q1[0];
cp(-pi/268435456) q1[28],q1[0];
cp(-pi/536870912) q1[29],q1[0];
cp(-pi/1073741824) q1[30],q1[0];
cp(-pi/256) q1[9],q1[1];
cp(-pi/512) q1[10],q1[1];
cp(-pi/1024) q1[11],q1[1];
cp(-pi/2048) q1[12],q1[1];
cp(-pi/4096) q1[13],q1[1];
cp(-pi/8192) q1[14],q1[1];
cp(-pi/16384) q1[15],q1[1];
cp(-pi/32768) q1[16],q1[1];
cp(-pi/65536) q1[17],q1[1];
cp(-pi/131072) q1[18],q1[1];
cp(-pi/262144) q1[19],q1[1];
cp(-pi/524288) q1[20],q1[1];
cp(-pi/1048576) q1[21],q1[1];
cp(-pi/2097152) q1[22],q1[1];
cp(-pi/4194304) q1[23],q1[1];
cp(-pi/8388608) q1[24],q1[1];
cp(-pi/16777216) q1[25],q1[1];
cp(-pi/33554432) q1[26],q1[1];
cp(-pi/67108864) q1[27],q1[1];
cp(-pi/134217728) q1[28],q1[1];
cp(-pi/268435456) q1[29],q1[1];
cp(-pi/536870912) q1[30],q1[1];
cp(-pi/128) q1[9],q1[2];
cp(-pi/256) q1[10],q1[2];
cp(-pi/512) q1[11],q1[2];
cp(-pi/1024) q1[12],q1[2];
cp(-pi/2048) q1[13],q1[2];
cp(-pi/4096) q1[14],q1[2];
cp(-pi/8192) q1[15],q1[2];
cp(-pi/16384) q1[16],q1[2];
cp(-pi/32768) q1[17],q1[2];
cp(-pi/65536) q1[18],q1[2];
cp(-pi/131072) q1[19],q1[2];
cp(-pi/262144) q1[20],q1[2];
cp(-pi/524288) q1[21],q1[2];
cp(-pi/1048576) q1[22],q1[2];
cp(-pi/2097152) q1[23],q1[2];
cp(-pi/4194304) q1[24],q1[2];
cp(-pi/8388608) q1[25],q1[2];
cp(-pi/16777216) q1[26],q1[2];
cp(-pi/33554432) q1[27],q1[2];
cp(-pi/67108864) q1[28],q1[2];
cp(-pi/134217728) q1[29],q1[2];
cp(-pi/268435456) q1[30],q1[2];
cp(-pi/64) q1[9],q1[3];
cp(-pi/128) q1[10],q1[3];
cp(-pi/256) q1[11],q1[3];
cp(-pi/512) q1[12],q1[3];
cp(-pi/1024) q1[13],q1[3];
cp(-pi/2048) q1[14],q1[3];
cp(-pi/4096) q1[15],q1[3];
cp(-pi/8192) q1[16],q1[3];
cp(-pi/16384) q1[17],q1[3];
cp(-pi/32768) q1[18],q1[3];
cp(-pi/65536) q1[19],q1[3];
cp(-pi/131072) q1[20],q1[3];
cp(-pi/262144) q1[21],q1[3];
cp(-pi/524288) q1[22],q1[3];
cp(-pi/1048576) q1[23],q1[3];
cp(-pi/2097152) q1[24],q1[3];
cp(-pi/4194304) q1[25],q1[3];
cp(-pi/8388608) q1[26],q1[3];
cp(-pi/16777216) q1[27],q1[3];
cp(-pi/33554432) q1[28],q1[3];
cp(-pi/67108864) q1[29],q1[3];
cp(-pi/134217728) q1[30],q1[3];
cp(-pi/32) q1[9],q1[4];
cp(-pi/64) q1[10],q1[4];
cp(-pi/128) q1[11],q1[4];
cp(-pi/256) q1[12],q1[4];
cp(-pi/512) q1[13],q1[4];
cp(-pi/1024) q1[14],q1[4];
cp(-pi/2048) q1[15],q1[4];
cp(-pi/4096) q1[16],q1[4];
cp(-pi/8192) q1[17],q1[4];
cp(-pi/16384) q1[18],q1[4];
cp(-pi/32768) q1[19],q1[4];
cp(-pi/65536) q1[20],q1[4];
cp(-pi/131072) q1[21],q1[4];
cp(-pi/262144) q1[22],q1[4];
cp(-pi/524288) q1[23],q1[4];
cp(-pi/1048576) q1[24],q1[4];
cp(-pi/2097152) q1[25],q1[4];
cp(-pi/4194304) q1[26],q1[4];
cp(-pi/8388608) q1[27],q1[4];
cp(-pi/16777216) q1[28],q1[4];
cp(-pi/33554432) q1[29],q1[4];
cp(-pi/67108864) q1[30],q1[4];
cp(-pi/16) q1[9],q1[5];
cp(-pi/32) q1[10],q1[5];
cp(-pi/64) q1[11],q1[5];
cp(-pi/128) q1[12],q1[5];
cp(-pi/256) q1[13],q1[5];
cp(-pi/512) q1[14],q1[5];
cp(-pi/1024) q1[15],q1[5];
cp(-pi/2048) q1[16],q1[5];
cp(-pi/4096) q1[17],q1[5];
cp(-pi/8192) q1[18],q1[5];
cp(-pi/16384) q1[19],q1[5];
cp(-pi/32768) q1[20],q1[5];
cp(-pi/65536) q1[21],q1[5];
cp(-pi/131072) q1[22],q1[5];
cp(-pi/262144) q1[23],q1[5];
cp(-pi/524288) q1[24],q1[5];
cp(-pi/1048576) q1[25],q1[5];
cp(-pi/2097152) q1[26],q1[5];
cp(-pi/4194304) q1[27],q1[5];
cp(-pi/8388608) q1[28],q1[5];
cp(-pi/16777216) q1[29],q1[5];
cp(-pi/33554432) q1[30],q1[5];
cp(-pi/8) q1[9],q1[6];
cp(-pi/16) q1[10],q1[6];
cp(-pi/32) q1[11],q1[6];
cp(-pi/64) q1[12],q1[6];
cp(-pi/128) q1[13],q1[6];
cp(-pi/256) q1[14],q1[6];
cp(-pi/512) q1[15],q1[6];
cp(-pi/1024) q1[16],q1[6];
cp(-pi/2048) q1[17],q1[6];
cp(-pi/4096) q1[18],q1[6];
cp(-pi/8192) q1[19],q1[6];
cp(-pi/16384) q1[20],q1[6];
cp(-pi/32768) q1[21],q1[6];
cp(-pi/65536) q1[22],q1[6];
cp(-pi/131072) q1[23],q1[6];
cp(-pi/262144) q1[24],q1[6];
cp(-pi/524288) q1[25],q1[6];
cp(-pi/1048576) q1[26],q1[6];
cp(-pi/2097152) q1[27],q1[6];
cp(-pi/4194304) q1[28],q1[6];
cp(-pi/8388608) q1[29],q1[6];
cp(-pi/16777216) q1[30],q1[6];
cp(-pi/4) q1[9],q1[7];
cp(-pi/8) q1[10],q1[7];
cp(-pi/16) q1[11],q1[7];
cp(-pi/32) q1[12],q1[7];
cp(-pi/64) q1[13],q1[7];
cp(-pi/128) q1[14],q1[7];
cp(-pi/256) q1[15],q1[7];
cp(-pi/512) q1[16],q1[7];
cp(-pi/1024) q1[17],q1[7];
cp(-pi/2048) q1[18],q1[7];
cp(-pi/4096) q1[19],q1[7];
cp(-pi/8192) q1[20],q1[7];
cp(-pi/16384) q1[21],q1[7];
cp(-pi/32768) q1[22],q1[7];
cp(-pi/65536) q1[23],q1[7];
cp(-pi/131072) q1[24],q1[7];
cp(-pi/262144) q1[25],q1[7];
cp(-pi/524288) q1[26],q1[7];
cp(-pi/1048576) q1[27],q1[7];
cp(-pi/2097152) q1[28],q1[7];
cp(-pi/4194304) q1[29],q1[7];
cp(-pi/8388608) q1[30],q1[7];
cp(-pi/2) q1[9],q1[8];
cp(-pi/4) q1[10],q1[8];
cp(-pi/8) q1[11],q1[8];
cp(-pi/16) q1[12],q1[8];
cp(-pi/32) q1[13],q1[8];
cp(-pi/64) q1[14],q1[8];
cp(-pi/128) q1[15],q1[8];
cp(-pi/256) q1[16],q1[8];
cp(-pi/512) q1[17],q1[8];
cp(-pi/1024) q1[18],q1[8];
cp(-pi/2048) q1[19],q1[8];
cp(-pi/4096) q1[20],q1[8];
cp(-pi/8192) q1[21],q1[8];
cp(-pi/16384) q1[22],q1[8];
cp(-pi/32768) q1[23],q1[8];
cp(-pi/65536) q1[24],q1[8];
cp(-pi/131072) q1[25],q1[8];
cp(-pi/262144) q1[26],q1[8];
cp(-pi/524288) q1[27],q1[8];
cp(-pi/1048576) q1[28],q1[8];
cp(-pi/2097152) q1[29],q1[8];
cp(-pi/4194304) q1[30],q1[8];
h q1[9];
cp(-pi/2) q1[10],q1[9];
h q1[10];
cp(-pi/4) q1[11],q1[9];
cp(-pi/2) q1[11],q1[10];
h q1[11];
cp(-pi/8) q1[12],q1[9];
cp(-pi/4) q1[12],q1[10];
cp(-pi/2) q1[12],q1[11];
h q1[12];
cp(-pi/16) q1[13],q1[9];
cp(-pi/8) q1[13],q1[10];
cp(-pi/4) q1[13],q1[11];
cp(-pi/2) q1[13],q1[12];
h q1[13];
cp(-pi/32) q1[14],q1[9];
cp(-pi/16) q1[14],q1[10];
cp(-pi/8) q1[14],q1[11];
cp(-pi/4) q1[14],q1[12];
cp(-pi/2) q1[14],q1[13];
h q1[14];
cp(-pi/64) q1[15],q1[9];
cp(-pi/32) q1[15],q1[10];
cp(-pi/16) q1[15],q1[11];
cp(-pi/8) q1[15],q1[12];
cp(-pi/4) q1[15],q1[13];
cp(-pi/2) q1[15],q1[14];
h q1[15];
cp(-pi/128) q1[16],q1[9];
cp(-pi/64) q1[16],q1[10];
cp(-pi/32) q1[16],q1[11];
cp(-pi/16) q1[16],q1[12];
cp(-pi/8) q1[16],q1[13];
cp(-pi/4) q1[16],q1[14];
cp(-pi/2) q1[16],q1[15];
h q1[16];
cp(-pi/256) q1[17],q1[9];
cp(-pi/128) q1[17],q1[10];
cp(-pi/64) q1[17],q1[11];
cp(-pi/32) q1[17],q1[12];
cp(-pi/16) q1[17],q1[13];
cp(-pi/8) q1[17],q1[14];
cp(-pi/4) q1[17],q1[15];
cp(-pi/2) q1[17],q1[16];
h q1[17];
cp(-pi/512) q1[18],q1[9];
cp(-pi/256) q1[18],q1[10];
cp(-pi/128) q1[18],q1[11];
cp(-pi/64) q1[18],q1[12];
cp(-pi/32) q1[18],q1[13];
cp(-pi/16) q1[18],q1[14];
cp(-pi/8) q1[18],q1[15];
cp(-pi/4) q1[18],q1[16];
cp(-pi/2) q1[18],q1[17];
h q1[18];
cp(-pi/1024) q1[19],q1[9];
cp(-pi/512) q1[19],q1[10];
cp(-pi/256) q1[19],q1[11];
cp(-pi/128) q1[19],q1[12];
cp(-pi/64) q1[19],q1[13];
cp(-pi/32) q1[19],q1[14];
cp(-pi/16) q1[19],q1[15];
cp(-pi/8) q1[19],q1[16];
cp(-pi/4) q1[19],q1[17];
cp(-pi/2) q1[19],q1[18];
h q1[19];
cp(-pi/2048) q1[20],q1[9];
cp(-pi/1024) q1[20],q1[10];
cp(-pi/512) q1[20],q1[11];
cp(-pi/256) q1[20],q1[12];
cp(-pi/128) q1[20],q1[13];
cp(-pi/64) q1[20],q1[14];
cp(-pi/32) q1[20],q1[15];
cp(-pi/16) q1[20],q1[16];
cp(-pi/8) q1[20],q1[17];
cp(-pi/4) q1[20],q1[18];
cp(-pi/2) q1[20],q1[19];
h q1[20];
cp(-pi/4096) q1[21],q1[9];
cp(-pi/2048) q1[21],q1[10];
cp(-pi/1024) q1[21],q1[11];
cp(-pi/512) q1[21],q1[12];
cp(-pi/256) q1[21],q1[13];
cp(-pi/128) q1[21],q1[14];
cp(-pi/64) q1[21],q1[15];
cp(-pi/32) q1[21],q1[16];
cp(-pi/16) q1[21],q1[17];
cp(-pi/8) q1[21],q1[18];
cp(-pi/4) q1[21],q1[19];
cp(-pi/2) q1[21],q1[20];
h q1[21];
cp(-pi/8192) q1[22],q1[9];
cp(-pi/4096) q1[22],q1[10];
cp(-pi/2048) q1[22],q1[11];
cp(-pi/1024) q1[22],q1[12];
cp(-pi/512) q1[22],q1[13];
cp(-pi/256) q1[22],q1[14];
cp(-pi/128) q1[22],q1[15];
cp(-pi/64) q1[22],q1[16];
cp(-pi/32) q1[22],q1[17];
cp(-pi/16) q1[22],q1[18];
cp(-pi/8) q1[22],q1[19];
cp(-pi/4) q1[22],q1[20];
cp(-pi/2) q1[22],q1[21];
h q1[22];
cp(-pi/16384) q1[23],q1[9];
cp(-pi/8192) q1[23],q1[10];
cp(-pi/4096) q1[23],q1[11];
cp(-pi/2048) q1[23],q1[12];
cp(-pi/1024) q1[23],q1[13];
cp(-pi/512) q1[23],q1[14];
cp(-pi/256) q1[23],q1[15];
cp(-pi/128) q1[23],q1[16];
cp(-pi/64) q1[23],q1[17];
cp(-pi/32) q1[23],q1[18];
cp(-pi/16) q1[23],q1[19];
cp(-pi/8) q1[23],q1[20];
cp(-pi/4) q1[23],q1[21];
cp(-pi/2) q1[23],q1[22];
h q1[23];
cp(-pi/32768) q1[24],q1[9];
cp(-pi/16384) q1[24],q1[10];
cp(-pi/8192) q1[24],q1[11];
cp(-pi/4096) q1[24],q1[12];
cp(-pi/2048) q1[24],q1[13];
cp(-pi/1024) q1[24],q1[14];
cp(-pi/512) q1[24],q1[15];
cp(-pi/256) q1[24],q1[16];
cp(-pi/128) q1[24],q1[17];
cp(-pi/64) q1[24],q1[18];
cp(-pi/32) q1[24],q1[19];
cp(-pi/16) q1[24],q1[20];
cp(-pi/8) q1[24],q1[21];
cp(-pi/4) q1[24],q1[22];
cp(-pi/2) q1[24],q1[23];
h q1[24];
cp(-pi/65536) q1[25],q1[9];
cp(-pi/32768) q1[25],q1[10];
cp(-pi/16384) q1[25],q1[11];
cp(-pi/8192) q1[25],q1[12];
cp(-pi/4096) q1[25],q1[13];
cp(-pi/2048) q1[25],q1[14];
cp(-pi/1024) q1[25],q1[15];
cp(-pi/512) q1[25],q1[16];
cp(-pi/256) q1[25],q1[17];
cp(-pi/128) q1[25],q1[18];
cp(-pi/64) q1[25],q1[19];
cp(-pi/32) q1[25],q1[20];
cp(-pi/16) q1[25],q1[21];
cp(-pi/8) q1[25],q1[22];
cp(-pi/4) q1[25],q1[23];
cp(-pi/2) q1[25],q1[24];
h q1[25];
cp(-pi/131072) q1[26],q1[9];
cp(-pi/65536) q1[26],q1[10];
cp(-pi/32768) q1[26],q1[11];
cp(-pi/16384) q1[26],q1[12];
cp(-pi/8192) q1[26],q1[13];
cp(-pi/4096) q1[26],q1[14];
cp(-pi/2048) q1[26],q1[15];
cp(-pi/1024) q1[26],q1[16];
cp(-pi/512) q1[26],q1[17];
cp(-pi/256) q1[26],q1[18];
cp(-pi/128) q1[26],q1[19];
cp(-pi/64) q1[26],q1[20];
cp(-pi/32) q1[26],q1[21];
cp(-pi/16) q1[26],q1[22];
cp(-pi/8) q1[26],q1[23];
cp(-pi/4) q1[26],q1[24];
cp(-pi/2) q1[26],q1[25];
h q1[26];
cp(-pi/262144) q1[27],q1[9];
cp(-pi/131072) q1[27],q1[10];
cp(-pi/65536) q1[27],q1[11];
cp(-pi/32768) q1[27],q1[12];
cp(-pi/16384) q1[27],q1[13];
cp(-pi/8192) q1[27],q1[14];
cp(-pi/4096) q1[27],q1[15];
cp(-pi/2048) q1[27],q1[16];
cp(-pi/1024) q1[27],q1[17];
cp(-pi/512) q1[27],q1[18];
cp(-pi/256) q1[27],q1[19];
cp(-pi/128) q1[27],q1[20];
cp(-pi/64) q1[27],q1[21];
cp(-pi/32) q1[27],q1[22];
cp(-pi/16) q1[27],q1[23];
cp(-pi/8) q1[27],q1[24];
cp(-pi/4) q1[27],q1[25];
cp(-pi/2) q1[27],q1[26];
h q1[27];
cp(-pi/524288) q1[28],q1[9];
cp(-pi/262144) q1[28],q1[10];
cp(-pi/131072) q1[28],q1[11];
cp(-pi/65536) q1[28],q1[12];
cp(-pi/32768) q1[28],q1[13];
cp(-pi/16384) q1[28],q1[14];
cp(-pi/8192) q1[28],q1[15];
cp(-pi/4096) q1[28],q1[16];
cp(-pi/2048) q1[28],q1[17];
cp(-pi/1024) q1[28],q1[18];
cp(-pi/512) q1[28],q1[19];
cp(-pi/256) q1[28],q1[20];
cp(-pi/128) q1[28],q1[21];
cp(-pi/64) q1[28],q1[22];
cp(-pi/32) q1[28],q1[23];
cp(-pi/16) q1[28],q1[24];
cp(-pi/8) q1[28],q1[25];
cp(-pi/4) q1[28],q1[26];
cp(-pi/2) q1[28],q1[27];
h q1[28];
cp(-pi/1048576) q1[29],q1[9];
cp(-pi/524288) q1[29],q1[10];
cp(-pi/262144) q1[29],q1[11];
cp(-pi/131072) q1[29],q1[12];
cp(-pi/65536) q1[29],q1[13];
cp(-pi/32768) q1[29],q1[14];
cp(-pi/16384) q1[29],q1[15];
cp(-pi/8192) q1[29],q1[16];
cp(-pi/4096) q1[29],q1[17];
cp(-pi/2048) q1[29],q1[18];
cp(-pi/1024) q1[29],q1[19];
cp(-pi/512) q1[29],q1[20];
cp(-pi/256) q1[29],q1[21];
cp(-pi/128) q1[29],q1[22];
cp(-pi/64) q1[29],q1[23];
cp(-pi/32) q1[29],q1[24];
cp(-pi/16) q1[29],q1[25];
cp(-pi/8) q1[29],q1[26];
cp(-pi/4) q1[29],q1[27];
cp(-pi/2) q1[29],q1[28];
h q1[29];
cp(-pi/2097152) q1[30],q1[9];
cp(-pi/1048576) q1[30],q1[10];
cp(-pi/524288) q1[30],q1[11];
cp(-pi/262144) q1[30],q1[12];
cp(-pi/131072) q1[30],q1[13];
cp(-pi/65536) q1[30],q1[14];
cp(-pi/32768) q1[30],q1[15];
cp(-pi/16384) q1[30],q1[16];
cp(-pi/8192) q1[30],q1[17];
cp(-pi/4096) q1[30],q1[18];
cp(-pi/2048) q1[30],q1[19];
cp(-pi/1024) q1[30],q1[20];
cp(-pi/512) q1[30],q1[21];
cp(-pi/256) q1[30],q1[22];
cp(-pi/128) q1[30],q1[23];
cp(-pi/64) q1[30],q1[24];
cp(-pi/32) q1[30],q1[25];
cp(-pi/16) q1[30],q1[26];
cp(-pi/8) q1[30],q1[27];
cp(-pi/4) q1[30],q1[28];
cp(-pi/2) q1[30],q1[29];
h q1[30];
