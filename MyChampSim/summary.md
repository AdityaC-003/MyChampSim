## IPC Statistics over SPEC traces

The values in the table represent $(\frac{IPC_{new\_policy}}{IPC_{mockingjay}} - 1) * 100$.

| Policy | hawkeye | lru | new_policy |
| --- | --- | --- | --- |
| astar_163B | -0.064 | -0.099 | 0.001 |
| astar_23B | 0.252 | 0.376 | -0.250 |
| astar_313B | -1.233 | -11.306 | -4.563 |
| bwaves_1609B | -0.835 | -3.349 | -2.284 |
| bwaves_1861B | -0.869 | -3.507 | -2.497 |
| bwaves_98B | -0.085 | -0.112 | -0.003 |
| bzip2_183B | -0.289 | -1.695 | -0.000 |
| bzip2_259B | -0.568 | -2.352 | -0.006 |
| bzip2_281B | -0.572 | -2.307 | -0.096 |
| cactusADM_1039B | -2.511 | -7.446 | -0.417 |
| cactusADM_1495B | -2.529 | -7.371 | -0.379 |
| cactusADM_734B | -2.282 | -6.969 | -0.166 |
| gcc_13B | 0.087 | -0.751 | -0.498 |
| gcc_39B | -0.052 | -0.148 | -0.000 |
| gcc_56B | 0.411 | -0.152 | 0.018 |
| h264ref_178B | -0.175 | -0.476 | -0.001 |
| h264ref_273B | -0.249 | -0.661 | 0.007 |
| h264ref_351B | -0.284 | -0.879 | 0.003 |
| lbm_1004B | -9.594 | -20.605 | -0.793 |
| lbm_564B | -7.266 | -15.987 | -0.646 |
| lbm_94B | -10.118 | -20.782 | -0.996 |
| sphinx3_1339B | -6.070 | -22.599 | 0.001 |
| sphinx3_2520B | -13.106 | -26.361 | -0.008 |
| sphinx3_883B | -3.056 | -17.582 | 0.045 |
| tonto_2049B | 0.000 | 0.000 | 0.000 |
| tonto_2834B | 0.123 | -0.240 | -0.001 |
| tonto_422B | -0.734 | -1.446 | -0.015 |
| wrf_1212B | 0.608 | 0.220 | 0.043 |
| wrf_1228B | -0.050 | -0.168 | 0.021 |
| wrf_1650B | 0.143 | -1.465 | -0.211 |
| xalancbmk_748B | -0.318 | -2.041 | -0.623 |
| xalancbmk_768B | -0.040 | -1.660 | -0.720 |
| xalancbmk_99B | -2.985 | -9.758 | -0.032 |
| zeusmp_100B | -0.014 | 0.092 | -0.026 |
| zeusmp_300B | -1.142 | -0.424 | -0.096 |
| zeusmp_600B | -0.011 | -0.050 | -0.071 |

- In most cases, mockingjay is better than the new policy. The cases where the new policy has a positive value have minimal improvement, and also have minimal predictions from the DBP. The cases where mockingjay is better than the new policy have a large improvement, and also have fairly high predictions from the DBP.

- This shows that the new policy is not as good as mockingjay, and mockingjay is better at dead block prediction that the newly implemented DBP functionality.

