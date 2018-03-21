def tree(vals):
    avg_iH1, avg_iH2, norm_std_a1, norm_max_a1, norm_std_window10_a1, norm_max_window10_a1, norm_std_a2, norm_max_a2, norm_std_window10_a2, norm_max_window10_a2, norm_std_a3, norm_max_a3, norm_std_window10_a3, norm_max_window10_a3, avg_ecross1, std_ecross1, max_ecross1, min_ecross1, avg_ecross2, std_ecross2, max_ecross2, min_ecross2, avg_ecross3, std_ecross3, max_ecross3, min_ecross3, norm_a1_slope, norm_a2_slope, norm_a3_slope, avg_beta12, std_beta12, min_beta12, max_beta12, avg_beta23, std_beta23, min_beta23, max_beta23 = vals
    #New booster
    if std_beta12 < 0.152237:
        if std_beta23 < 0.0269198:
            if min_ecross2 < 0.553545:
                if avg_ecross1 < 0.475498:
                    if avg_iH2 < 7.18684:
                        if max_ecross3 < 0.213699:
                            if avg_ecross2 < 0.412932:
                                return 0.123982
                            else: #threshold avg_ecross2 > 0.412932
                                if norm_std_a1 < 4.1612e-05:
                                    if max_ecross1 < 0.144902:
                                        if max_beta12 < 7.47163:
                                            return 0.36563
                                        else: #threshold max_beta12 > 7.47163
                                            return 0.123982
                                    else: #threshold max_ecross1 > 0.144902
                                        if norm_a3_slope < 2.78577e-12:
                                            return 0.126263
                                        else: #threshold norm_a3_slope > 2.78577e-12
                                            if norm_max_a2 < 0.00101502:
                                                if avg_iH2 < 21.4114:
                                                    if min_beta12 < 6.07216:
                                                        if norm_a2_slope < -6.51951e-12:
                                                            return -0.170113
                                                        else: #threshold norm_a2_slope > -6.51951e-12
                                                            if std_beta12 < 0.0194068:
                                                                return -0.200261
                                                            else: #threshold std_beta12 > 0.0194068
                                                                if min_beta23 < 21.4587:
                                                                    if avg_ecross3 < 0.662709:
                                                                        if avg_ecross1 < 0.31633:
                                                                            return 0.0621609
                                                                        else: #threshold avg_ecross1 > 0.31633
                                                                            return -0.359289
                                                                    else: #threshold avg_ecross3 > 0.662709
                                                                        if min_beta12 < 4.73346:
                                                                            return -0.109323
                                                                        else: #threshold min_beta12 > 4.73346
                                                                            if avg_iH2 < 0.0944279:
                                                                                return 0.316962
                                                                            else: #threshold avg_iH2 > 0.0944279
                                                                                return 0.0720043
                                                                else: #threshold min_beta23 > 21.4587
                                                                    if min_ecross2 < 0.309655:
                                                                        if max_ecross1 < 0.816824:
                                                                            return 0.26402
                                                                        else: #threshold max_ecross1 > 0.816824
                                                                            if norm_std_window10_a2 < 2.87538e-05:
                                                                                if avg_ecross1 < 0.390162:
                                                                                    if std_ecross2 < 0.00597682:
                                                                                        return 0.377157
                                                                                    else: #threshold std_ecross2 > 0.00597682
                                                                                        return 0.250621
                                                                                else: #threshold avg_ecross1 > 0.390162
                                                                                    if min_ecross3 < 0.0183671:
                                                                                        return 0.366438
                                                                                    else: #threshold min_ecross3 > 0.0183671
                                                                                        return 0.237755
                                                                            else: #threshold norm_std_window10_a2 > 2.87538e-05
                                                                                if norm_std_a3 < 1.33561e-05:
                                                                                    return -0.364816
                                                                                else: #threshold norm_std_a3 > 1.33561e-05
                                                                                    return -0.39191
                                                                    else: #threshold min_ecross2 > 0.309655
                                                                        if std_ecross2 < 0.0269234:
                                                                            return 0.250621
                                                                        else: #threshold std_ecross2 > 0.0269234
                                                                            return 0.379548
                                                    else: #threshold min_beta12 > 6.07216
                                                        if min_beta23 < 21.9292:
                                                            if min_beta12 < 25.1852:
                                                                return 0.34296
                                                            else: #threshold min_beta12 > 25.1852
                                                                if std_beta23 < 0.00832886:
                                                                    if max_ecross1 < 0.202701:
                                                                        return 0.378413
                                                                    else: #threshold max_ecross1 > 0.202701
                                                                        if norm_max_window10_a1 < 0.000111966:
                                                                            return -0.109323
                                                                        else: #threshold norm_max_window10_a1 > 0.000111966
                                                                            if std_beta23 < 0.0508533:
                                                                                if avg_ecross2 < 1.27579:
                                                                                    return 0.0930193
                                                                                else: #threshold avg_ecross2 > 1.27579
                                                                                    if avg_ecross1 < 0.585533:
                                                                                        if min_ecross2 < 0.39141:
                                                                                            if min_beta12 < 15.0871:
                                                                                                if min_ecross3 < 0.114959:
                                                                                                    return -0.377455
                                                                                                else: #threshold min_ecross3 > 0.114959
                                                                                                    return 0.170695
                                                                                            else: #threshold min_beta12 > 15.0871
                                                                                                return -0.377046
                                                                                        else: #threshold min_ecross2 > 0.39141
                                                                                            return 0.0266125
                                                                                    else: #threshold avg_ecross1 > 0.585533
                                                                                        if max_ecross3 < 0.455792:
                                                                                            return -0.0476705
                                                                                        else: #threshold max_ecross3 > 0.455792
                                                                                            if norm_a2_slope < 2.75124e-11:
                                                                                                return 0.225392
                                                                                            else: #threshold norm_a2_slope > 2.75124e-11
                                                                                                return 0.18643
                                                                            else: #threshold std_beta23 > 0.0508533
                                                                                if std_beta23 < 0.0199795:
                                                                                    if avg_iH1 < 6.84618:
                                                                                        return 0.375246
                                                                                    else: #threshold avg_iH1 > 6.84618
                                                                                        if max_ecross3 < 0.350056:
                                                                                            if norm_max_window10_a3 < 0.000240676:
                                                                                                return 0.141281
                                                                                            else: #threshold norm_max_window10_a3 > 0.000240676
                                                                                                return -0.122703
                                                                                        else: #threshold max_ecross3 > 0.350056
                                                                                            return -0.365942
                                                                                else: #threshold std_beta23 > 0.0199795
                                                                                    return 0.365795
                                                                else: #threshold std_beta23 > 0.00832886
                                                                    if norm_std_a3 < 0.00173155:
                                                                        return 0.213502
                                                                    else: #threshold norm_std_a3 > 0.00173155
                                                                        return 0.357629
                                                        else: #threshold min_beta23 > 21.9292
                                                            return -0.385275
                                                else: #threshold avg_iH2 > 21.4114
                                                    return 0.0185724
                                            else: #threshold norm_max_a2 > 0.00101502
                                                return -0.392496
                                else: #threshold norm_std_a1 > 4.1612e-05
                                    if norm_a2_slope < 2.2288e-10:
                                        return 0.375222
                                    else: #threshold norm_a2_slope > 2.2288e-10
                                        return 0.289509
                        else: #threshold max_ecross3 > 0.213699
                            if std_beta23 < 0.0547796:
                                if min_ecross2 < 0.00694028:
                                    return 0.0266125
                                else: #threshold min_ecross2 > 0.00694028
                                    return 0.0527237
                            else: #threshold std_beta23 > 0.0547796
                                if min_beta23 < 22.0207:
                                    return 0.0185724
                                else: #threshold min_beta23 > 22.0207
                                    if std_beta23 < 0.00864602:
                                        return 0.360682
                                    else: #threshold std_beta23 > 0.00864602
                                        return -0.36972
                    else: #threshold avg_iH2 > 7.18684
                        if norm_max_a2 < 0.000220137:
                            return 0.0448777
                        else: #threshold norm_max_a2 > 0.000220137
                            return 0.295324
                else: #threshold avg_ecross1 > 0.475498
                    if min_ecross2 < 0.00204883:
                        return 0.28706
                    else: #threshold min_ecross2 > 0.00204883
                        return 0.375116
            else: #threshold min_ecross2 > 0.553545
                return 0.375113
        else: #threshold std_beta23 > 0.0269198
            if std_beta12 < 0.0197297:
                return 0.0720043
            else: #threshold std_beta12 > 0.0197297
                if avg_ecross2 < 0.649205:
                    return -0.170113
                else: #threshold avg_ecross2 > 0.649205
                    if norm_max_window10_a1 < 0.000113902:
                        if max_ecross1 < 0.627707:
                            return 0.250621
                        else: #threshold max_ecross1 > 0.627707
                            if norm_max_a2 < 7.29912e-05:
                                if max_ecross3 < 0.118902:
                                    return -0.364816
                                else: #threshold max_ecross3 > 0.118902
                                    if norm_a2_slope < 9.12654e-11:
                                        return -0.109323
                                    else: #threshold norm_a2_slope > 9.12654e-11
                                        return -0.394913
                            else: #threshold norm_max_a2 > 7.29912e-05
                                if min_beta12 < 16.9096:
                                    return 0.0436681
                                else: #threshold min_beta12 > 16.9096
                                    return -0.178491
                    else: #threshold norm_max_window10_a1 > 0.000113902
                        if min_ecross2 < 0.0356028:
                            if avg_ecross2 < 0.0586459:
                                return 0.280349
                            else: #threshold avg_ecross2 > 0.0586459
                                return 0.0436681
                        else: #threshold min_ecross2 > 0.0356028
                            if norm_std_a1 < 5.03706e-05:
                                return 0.0822807
                            else: #threshold norm_std_a1 > 5.03706e-05
                                if avg_iH2 < 0.292269:
                                    if std_beta23 < 0.0123284:
                                        if std_ecross2 < 0.0707805:
                                            return 0.0822807
                                        else: #threshold std_ecross2 > 0.0707805
                                            return 0.0436681
                                    else: #threshold std_beta23 > 0.0123284
                                        if min_ecross1 < 0.155437:
                                            return 0.0930193
                                        else: #threshold min_ecross1 > 0.155437
                                            if std_beta12 < 0.0175644:
                                                if norm_max_a2 < 1.99548e-05:
                                                    return -0.377845
                                                else: #threshold norm_max_a2 > 1.99548e-05
                                                    if avg_ecross1 < 0.245846:
                                                        if norm_max_a2 < 3.13849e-05:
                                                            if avg_ecross2 < 0.157539:
                                                                return 0.0720043
                                                            else: #threshold avg_ecross2 > 0.157539
                                                                return 0.116014
                                                        else: #threshold norm_max_a2 > 3.13849e-05
                                                            return 0.363942
                                                    else: #threshold avg_ecross1 > 0.245846
                                                        return 0.340324
                                            else: #threshold std_beta12 > 0.0175644
                                                return 0.357754
                                else: #threshold avg_iH2 > 0.292269
                                    if max_ecross1 < 0.842877:
                                        if std_ecross2 < 0.0588829:
                                            if avg_ecross2 < 0.481899:
                                                return 0.141281
                                            else: #threshold avg_ecross2 > 0.481899
                                                return -0.360851
                                        else: #threshold std_ecross2 > 0.0588829
                                            if avg_ecross3 < 0.395037:
                                                return 0.375554
                                            else: #threshold avg_ecross3 > 0.395037
                                                if min_beta12 < 26.3844:
                                                    if norm_max_window10_a1 < 9.56949e-05:
                                                        return -0.109323
                                                    else: #threshold norm_max_window10_a1 > 9.56949e-05
                                                        return -0.368423
                                                else: #threshold min_beta12 > 26.3844
                                                    return 0.326995
                                    else: #threshold max_ecross1 > 0.842877
                                        if norm_a2_slope < -1.75797e-10:
                                            return 0.320138
                                        else: #threshold norm_a2_slope > -1.75797e-10
                                            return 0.128215
    else: #threshold std_beta12 > 0.152237
        if max_ecross1 < 0.375108:
            if avg_ecross2 < 0.472345:
                if min_ecross3 < 0.252015:
                    return 0.141281
                else: #threshold min_ecross3 > 0.252015
                    if min_beta12 < 4.33733:
                        return -0.0107403
                    else: #threshold min_beta12 > 4.33733
                        if norm_std_a1 < 0.00013575:
                            if norm_max_a2 < 5.62409e-05:
                                if max_ecross1 < 0.0509703:
                                    if min_ecross2 < 0.044199:
                                        if std_beta12 < 0.0676202:
                                            return 0.325058
                                        else: #threshold std_beta12 > 0.0676202
                                            return 0.128343
                                    else: #threshold min_ecross2 > 0.044199
                                        return 0.250621
                                else: #threshold max_ecross1 > 0.0509703
                                    return 0.367294
                            else: #threshold norm_max_a2 > 5.62409e-05
                                if norm_a2_slope < -5.76624e-11:
                                    return 0.116014
                                else: #threshold norm_a2_slope > -5.76624e-11
                                    if min_beta23 < 14.9249:
                                        return 0.194631
                                    else: #threshold min_beta23 > 14.9249
                                        return -0.370896
                        else: #threshold norm_std_a1 > 0.00013575
                            return 0.26402
            else: #threshold avg_ecross2 > 0.472345
                if norm_a2_slope < -5.38653e-11:
                    if avg_ecross1 < 0.613302:
                        return -0.14058
                    else: #threshold avg_ecross1 > 0.613302
                        if std_ecross2 < 0.0876347:
                            return 0.268269
                        else: #threshold std_ecross2 > 0.0876347
                            if avg_iH2 < 0.733143:
                                return -0.109323
                            else: #threshold avg_iH2 > 0.733143
                                return -0.391633
                else: #threshold norm_a2_slope > -5.38653e-11
                    if avg_ecross2 < 0.568949:
                        return -0.128935
                    else: #threshold avg_ecross2 > 0.568949
                        return 0.313819
        else: #threshold max_ecross1 > 0.375108
            if max_ecross1 < 0.109393:
                if norm_a2_slope < -7.3488e-11:
                    if norm_max_a2 < 0.000463064:
                        if avg_iH1 < 0.37004:
                            return 0.357754
                        else: #threshold avg_iH1 > 0.37004
                            return 0.225392
                    else: #threshold norm_max_a2 > 0.000463064
                        return 0.340324
                else: #threshold norm_a2_slope > -7.3488e-11
                    if max_ecross3 < 0.623492:
                        if norm_std_a3 < 0.000409566:
                            if avg_iH1 < 3.1446:
                                if avg_ecross2 < 0.312018:
                                    if max_ecross3 < 0.299093:
                                        return 0.141281
                                    else: #threshold max_ecross3 > 0.299093
                                        return 0.339023
                                else: #threshold avg_ecross2 > 0.312018
                                    if std_ecross2 < 0.0262941:
                                        return -0.35666
                                    else: #threshold std_ecross2 > 0.0262941
                                        if avg_iH1 < 1.2451:
                                            if avg_ecross3 < 0.735332:
                                                if avg_ecross3 < 1.15988:
                                                    if avg_ecross2 < 0.780637:
                                                        return 0.0822807
                                                    else: #threshold avg_ecross2 > 0.780637
                                                        return -0.0107403
                                                else: #threshold avg_ecross3 > 1.15988
                                                    if max_ecross3 < 0.17125:
                                                        return 0.250621
                                                    else: #threshold max_ecross3 > 0.17125
                                                        if std_beta23 < 0.116201:
                                                            return 0.340324
                                                        else: #threshold std_beta23 > 0.116201
                                                            return -0.372306
                                            else: #threshold avg_ecross3 > 0.735332
                                                return 0.392735
                                        else: #threshold avg_iH1 > 1.2451
                                            if std_beta12 < 0.0373641:
                                                return 0.338688
                                            else: #threshold std_beta12 > 0.0373641
                                                return 0.0822807
                            else: #threshold avg_iH1 > 3.1446
                                return -0.372952
                        else: #threshold norm_std_a3 > 0.000409566
                            return 0.104252
                    else: #threshold max_ecross3 > 0.623492
                        return 0.116014
            else: #threshold max_ecross1 > 0.109393
                if max_ecross1 < 0.0524725:
                    if norm_std_window10_a2 < 0.000161967:
                        return -0.14058
                    else: #threshold norm_std_window10_a2 > 0.000161967
                        if std_ecross3 < 0.00582288:
                            if std_beta12 < 0.0454933:
                                if norm_a2_slope < 1.31787e-09:
                                    return 0.31474
                                else: #threshold norm_a2_slope > 1.31787e-09
                                    return -0.116173
                            else: #threshold std_beta12 > 0.0454933
                                if norm_a2_slope < -3.425e-10:
                                    return 0.360682
                                else: #threshold norm_a2_slope > -3.425e-10
                                    return 0.141281
                        else: #threshold std_ecross3 > 0.00582288
                            return 0.250621
                else: #threshold max_ecross1 > 0.0524725
                    if norm_max_a2 < 0.000167089:
                        return 0.191039
                    else: #threshold norm_max_a2 > 0.000167089
                        return -0.0107403
    #New booster
    if std_beta12 < 0.152237:
        if max_ecross2 < 0.514873:
            if avg_ecross3 < 1.46353:
                return 0.0338133
            else: #threshold avg_ecross3 > 1.46353
                if norm_max_a2 < 0.000202965:
                    if avg_ecross2 < 0.396461:
                        if avg_iH1 < 0.25094:
                            if avg_iH2 < 1.23471:
                                return -0.328551
                            else: #threshold avg_iH2 > 1.23471
                                if norm_std_window10_a3 < 9.19727e-06:
                                    return -0.189789
                                else: #threshold norm_std_window10_a3 > 9.19727e-06
                                    if avg_ecross2 < 0.588318:
                                        return 0.181396
                                    else: #threshold avg_ecross2 > 0.588318
                                        return 0.312287
                        else: #threshold avg_iH1 > 0.25094
                            return 0.0762404
                    else: #threshold avg_ecross2 > 0.396461
                        return 0.0955989
                else: #threshold norm_max_a2 > 0.000202965
                    if max_beta23 < 11.6749:
                        if std_ecross1 < 0.0442218:
                            if max_ecross2 < 0.397214:
                                if avg_ecross3 < 0.149788:
                                    return 0.305118
                                else: #threshold avg_ecross3 > 0.149788
                                    return 0.16462
                            else: #threshold max_ecross2 > 0.397214
                                return 0.0043732
                        else: #threshold std_ecross1 > 0.0442218
                            if avg_ecross3 < 0.440577:
                                return 0.266177
                            else: #threshold avg_ecross3 > 0.440577
                                return 0.141693
                    else: #threshold max_beta23 > 11.6749
                        if norm_a3_slope < 7.65416e-11:
                            if norm_max_a2 < 0.000164888:
                                return 0.204499
                            else: #threshold norm_max_a2 > 0.000164888
                                if max_beta23 < 7.12135:
                                    if norm_max_window10_a1 < 0.000945899:
                                        if avg_beta12 < 6.69468:
                                            if max_ecross3 < 0.161319:
                                                if min_ecross3 < 0.00424474:
                                                    if avg_ecross1 < 0.388699:
                                                        return 0.0197767
                                                    else: #threshold avg_ecross1 > 0.388699
                                                        if std_ecross2 < 0.0125261:
                                                            if avg_ecross2 < 0.134834:
                                                                return 0.242215
                                                            else: #threshold avg_ecross2 > 0.134834
                                                                return -0.375495
                                                        else: #threshold std_ecross2 > 0.0125261
                                                            if norm_a2_slope < -2.04319e-10:
                                                                return -0.357694
                                                            else: #threshold norm_a2_slope > -2.04319e-10
                                                                return -0.0993267
                                                else: #threshold min_ecross3 > 0.00424474
                                                    return 0.312593
                                            else: #threshold max_ecross3 > 0.161319
                                                return 0.253838
                                        else: #threshold avg_beta12 > 6.69468
                                            if norm_max_a3 < 0.000356778:
                                                return 0.0406943
                                            else: #threshold norm_max_a3 > 0.000356778
                                                return -0.342949
                                    else: #threshold norm_max_window10_a1 > 0.000945899
                                        return 0.130886
                                else: #threshold max_beta23 > 7.12135
                                    return 0.146706
                        else: #threshold norm_a3_slope > 7.65416e-11
                            return 0.18328
        else: #threshold max_ecross2 > 0.514873
            if max_ecross3 < 0.311177:
                return 0.209864
            else: #threshold max_ecross3 > 0.311177
                if std_ecross3 < 0.0674332:
                    if avg_beta12 < 4.2403:
                        return 0.112733
                    else: #threshold avg_beta12 > 4.2403
                        return 0.272788
                else: #threshold std_ecross3 > 0.0674332
                    return 0.118874
    else: #threshold std_beta12 > 0.152237
        if std_beta12 < 0.0239702:
            if min_beta23 < 7.77732:
                if std_ecross2 < 0.0860255:
                    return 0.25084
                else: #threshold std_ecross2 > 0.0860255
                    if max_ecross3 < 0.581523:
                        if min_ecross1 < 0.416007:
                            if max_ecross2 < 0.624413:
                                if max_ecross2 < 0.113717:
                                    return 0.337405
                                else: #threshold max_ecross2 > 0.113717
                                    return 0.0446091
                            else: #threshold max_ecross2 > 0.624413
                                return 0.323881
                        else: #threshold min_ecross1 > 0.416007
                            if norm_a2_slope < -1.47823e-10:
                                return 0.147606
                            else: #threshold norm_a2_slope > -1.47823e-10
                                return 0.299845
                    else: #threshold max_ecross3 > 0.581523
                        if avg_beta12 < 8.19567:
                            if norm_max_window10_a2 < 0.00228626:
                                return -0.13879
                            else: #threshold norm_max_window10_a2 > 0.00228626
                                if avg_ecross1 < 0.32413:
                                    if max_ecross2 < 0.128373:
                                        return 0.317633
                                    else: #threshold max_ecross2 > 0.128373
                                        if avg_ecross2 < 0.72951:
                                            if norm_std_a1 < 8.78831e-05:
                                                if norm_std_a1 < 0.0016085:
                                                    if min_beta23 < 8.22768:
                                                        return 0.213238
                                                    else: #threshold min_beta23 > 8.22768
                                                        return 0.317562
                                                else: #threshold norm_std_a1 > 0.0016085
                                                    return 0.0789968
                                            else: #threshold norm_std_a1 > 8.78831e-05
                                                return -0.333345
                                        else: #threshold avg_ecross2 > 0.72951
                                            return 0.279598
                                else: #threshold avg_ecross1 > 0.32413
                                    if avg_beta12 < 19.9213:
                                        if std_ecross2 < 0.0146058:
                                            if std_ecross2 < 0.089562:
                                                return 0.0599024
                                            else: #threshold std_ecross2 > 0.089562
                                                return -0.120457
                                        else: #threshold std_ecross2 > 0.0146058
                                            if min_ecross1 < 0.127229:
                                                return -0.338163
                                            else: #threshold min_ecross1 > 0.127229
                                                if std_beta12 < 0.28122:
                                                    return 0.30188
                                                else: #threshold std_beta12 > 0.28122
                                                    if avg_beta12 < 12.998:
                                                        if avg_beta12 < 27.9531:
                                                            if min_ecross1 < 0.00684289:
                                                                return -0.36251
                                                            else: #threshold min_ecross1 > 0.00684289
                                                                if avg_ecross2 < 0.125443:
                                                                    return 0.322525
                                                                else: #threshold avg_ecross2 > 0.125443
                                                                    return 0.264774
                                                        else: #threshold avg_beta12 > 27.9531
                                                            return 0.113302
                                                    else: #threshold avg_beta12 > 12.998
                                                        if norm_std_window10_a1 < 0.000775363:
                                                            if std_ecross2 < 0.131424:
                                                                return 0.0970401
                                                            else: #threshold std_ecross2 > 0.131424
                                                                return -0.142667
                                                        else: #threshold norm_std_window10_a1 > 0.000775363
                                                            if std_ecross1 < 0.0259099:
                                                                return -0.331306
                                                            else: #threshold std_ecross1 > 0.0259099
                                                                return -0.0946665
                                    else: #threshold avg_beta12 > 19.9213
                                        return -0.00720539
                        else: #threshold avg_beta12 > 8.19567
                            return -0.357055
            else: #threshold min_beta23 > 7.77732
                if norm_a3_slope < 8.6123e-11:
                    if avg_beta12 < 17.2759:
                        if min_ecross2 < 0.00242762:
                            if std_ecross3 < 0.00913983:
                                return 0.10535
                            else: #threshold std_ecross3 > 0.00913983
                                if std_ecross1 < 0.0152585:
                                    if avg_beta12 < 15.721:
                                        return -0.110047
                                    else: #threshold avg_beta12 > 15.721
                                        return 0.132927
                                else: #threshold std_ecross1 > 0.0152585
                                    return 0.22294
                        else: #threshold min_ecross2 > 0.00242762
                            if min_beta23 < 20.1299:
                                if min_beta23 < 14.5923:
                                    return 0.148404
                                else: #threshold min_beta23 > 14.5923
                                    if avg_beta12 < -166.59:
                                        return 0.218224
                                    else: #threshold avg_beta12 > -166.59
                                        return 0.181199
                            else: #threshold min_beta23 > 20.1299
                                return -0.226449
                    else: #threshold avg_beta12 > 17.2759
                        return 0.116151
                else: #threshold norm_a3_slope > 8.6123e-11
                    return 0.17112
        else: #threshold std_beta12 > 0.0239702
            if std_ecross2 < 0.0499841:
                if norm_a2_slope < -3.32517e-10:
                    return 0.362322
                else: #threshold norm_a2_slope > -3.32517e-10
                    return -0.033339
            else: #threshold std_ecross2 > 0.0499841
                if max_ecross3 < 0.0394949:
                    if norm_a3_slope < -5.12638e-12:
                        if norm_a1_slope < 5.72817e-12:
                            return -0.334593
                        else: #threshold norm_a1_slope > 5.72817e-12
                            if norm_a2_slope < 9.38106e-11:
                                return 0.312921
                            else: #threshold norm_a2_slope > 9.38106e-11
                                return 0.215672
                    else: #threshold norm_a3_slope > -5.12638e-12
                        return 0.19863
                else: #threshold max_ecross3 > 0.0394949
                    return -0.104382
    #New booster
    if max_ecross2 < 0.517285:
        if norm_max_a2 < 0.00185824:
            if max_ecross1 < 0.901291:
                if max_ecross3 < 0.294738:
                    if std_ecross1 < 0.0619358:
                        return 0.290249
                    else: #threshold std_ecross1 > 0.0619358
                        if max_ecross1 < 0.460422:
                            if avg_beta23 < 17.9961:
                                return -0.315019
                            else: #threshold avg_beta23 > 17.9961
                                if min_beta12 < 26.5018:
                                    return -0.00504305
                                else: #threshold min_beta12 > 26.5018
                                    if avg_ecross1 < 0.479273:
                                        return 0.109708
                                    else: #threshold avg_ecross1 > 0.479273
                                        if std_ecross1 < 0.0392156:
                                            if norm_std_a3 < 0.00054964:
                                                if min_ecross2 < 0.00690278:
                                                    return 0.123591
                                                else: #threshold min_ecross2 > 0.00690278
                                                    if avg_ecross1 < 0.335187:
                                                        return -0.081691
                                                    else: #threshold avg_ecross1 > 0.335187
                                                        return 0.245861
                                            else: #threshold norm_std_a3 > 0.00054964
                                                if avg_iH1 < 1.61843:
                                                    if max_ecross2 < 0.134059:
                                                        if min_ecross3 < 0.00393097:
                                                            if max_ecross1 < 0.348072:
                                                                if avg_ecross3 < 0.0487864:
                                                                    return -0.290645
                                                                else: #threshold avg_ecross3 > 0.0487864
                                                                    if min_beta12 < 28.9687:
                                                                        if std_beta23 < 0.0170008:
                                                                            return -0.19886
                                                                        else: #threshold std_beta23 > 0.0170008
                                                                            if norm_std_window10_a2 < 0.00123607:
                                                                                return 0.0404378
                                                                            else: #threshold norm_std_window10_a2 > 0.00123607
                                                                                return 0.00398338
                                                                    else: #threshold min_beta12 > 28.9687
                                                                        return 0.26418
                                                            else: #threshold max_ecross1 > 0.348072
                                                                return 0.258398
                                                        else: #threshold min_ecross3 > 0.00393097
                                                            if std_ecross2 < 0.0500654:
                                                                return -0.350219
                                                            else: #threshold std_ecross2 > 0.0500654
                                                                return 0.10304
                                                    else: #threshold max_ecross2 > 0.134059
                                                        if min_ecross1 < 0.00762777:
                                                            return 0.281138
                                                        else: #threshold min_ecross1 > 0.00762777
                                                            if std_ecross2 < 0.0581657:
                                                                return -0.298343
                                                            else: #threshold std_ecross2 > 0.0581657
                                                                return 0.0560866
                                                else: #threshold avg_iH1 > 1.61843
                                                    if std_ecross2 < 0.0120138:
                                                        if norm_max_a2 < 0.00135025:
                                                            return 0.103194
                                                        else: #threshold norm_max_a2 > 0.00135025
                                                            if std_ecross2 < 0.215275:
                                                                if norm_std_window10_a3 < 2.76861e-05:
                                                                    return -0.195829
                                                                else: #threshold norm_std_window10_a3 > 2.76861e-05
                                                                    return 0.243734
                                                            else: #threshold std_ecross2 > 0.215275
                                                                if norm_std_window10_a2 < 0.000218247:
                                                                    return 0.286435
                                                                else: #threshold norm_std_window10_a2 > 0.000218247
                                                                    if norm_max_window10_a2 < 0.000748686:
                                                                        return 0.0812578
                                                                    else: #threshold norm_max_window10_a2 > 0.000748686
                                                                        return -0.205518
                                                    else: #threshold std_ecross2 > 0.0120138
                                                        return -0.36845
                                        else: #threshold std_ecross1 > 0.0392156
                                            return -0.0550036
                        else: #threshold max_ecross1 > 0.460422
                            if norm_max_a2 < 0.00137719:
                                return 0.0857531
                            else: #threshold norm_max_a2 > 0.00137719
                                return -0.336813
                else: #threshold max_ecross3 > 0.294738
                    if norm_a2_slope < 3.54782e-11:
                        return 0.278104
                    else: #threshold norm_a2_slope > 3.54782e-11
                        if norm_std_a1 < 0.000403288:
                            return -0.307938
                        else: #threshold norm_std_a1 > 0.000403288
                            if norm_max_a2 < -1.26525:
                                return 0.286852
                            else: #threshold norm_max_a2 > -1.26525
                                return 0.234141
            else: #threshold max_ecross1 > 0.901291
                if max_ecross1 < 0.215154:
                    if norm_std_a3 < 3.27594e-05:
                        if max_ecross1 < 0.61913:
                            if std_ecross2 < 0.00201382:
                                if norm_a3_slope < 2.7671e-11:
                                    if min_ecross3 < 0.000225592:
                                        return -0.308882
                                    else: #threshold min_ecross3 > 0.000225592
                                        return -0.300465
                                else: #threshold norm_a3_slope > 2.7671e-11
                                    return 0.178499
                            else: #threshold std_ecross2 > 0.00201382
                                return -0.402859
                        else: #threshold max_ecross1 > 0.61913
                            return -0.0834345
                    else: #threshold norm_std_a3 > 3.27594e-05
                        return 0.255721
                else: #threshold max_ecross1 > 0.215154
                    return 0.271674
        else: #threshold norm_max_a2 > 0.00185824
            if std_beta12 < 0.0232287:
                return 0.192491
            else: #threshold std_beta12 > 0.0232287
                return 0.0869398
    else: #threshold max_ecross2 > 0.517285
        if std_beta23 < 0.0200276:
            if min_ecross1 < 0.524135:
                if max_ecross2 < 0.180716:
                    return 0.284056
                else: #threshold max_ecross2 > 0.180716
                    return 0.25319
            else: #threshold min_ecross1 > 0.524135
                if min_ecross2 < 0.0400814:
                    if avg_iH1 < 0.62031:
                        if min_beta12 < 26.7583:
                            return 0.117433
                        else: #threshold min_beta12 > 26.7583
                            return -0.0485717
                    else: #threshold avg_iH1 > 0.62031
                        return -0.0787799
                else: #threshold min_ecross2 > 0.0400814
                    return 0.234697
        else: #threshold std_beta23 > 0.0200276
            if avg_ecross3 < 1.31841:
                return -0.177662
            else: #threshold avg_ecross3 > 1.31841
                if norm_a3_slope < -4.4085e-11:
                    return -0.0305391
                else: #threshold norm_a3_slope > -4.4085e-11
                    if norm_a3_slope < -8.34671e-11:
                        if norm_std_window10_a3 < 2.74173e-05:
                            if norm_max_a2 < 0.000935739:
                                return 0.229003
                            else: #threshold norm_max_a2 > 0.000935739
                                if min_beta12 < 21.6083:
                                    if max_ecross3 < 0.0580626:
                                        if max_beta12 < 12.0193:
                                            return 0.0124636
                                        else: #threshold max_beta12 > 12.0193
                                            return 0.0859245
                                    else: #threshold max_ecross3 > 0.0580626
                                        return 0.203383
                                else: #threshold min_beta12 > 21.6083
                                    return 0.191388
                        else: #threshold norm_std_window10_a3 > 2.74173e-05
                            if max_ecross3 < 0.155517:
                                if std_beta12 < 0.0193314:
                                    return -0.166416
                                else: #threshold std_beta12 > 0.0193314
                                    return -0.29333
                            else: #threshold max_ecross3 > 0.155517
                                if avg_iH1 < 0.323007:
                                    if max_ecross1 < 0.220563:
                                        if std_ecross2 < 0.00408348:
                                            return 0.130905
                                        else: #threshold std_ecross2 > 0.00408348
                                            return 0.29758
                                    else: #threshold max_ecross1 > 0.220563
                                        return 0.158064
                                else: #threshold avg_iH1 > 0.323007
                                    if norm_std_window10_a3 < 7.60251e-05:
                                        if norm_max_a2 < 0.00093073:
                                            return -0.148116
                                        else: #threshold norm_max_a2 > 0.00093073
                                            return 0.193627
                                    else: #threshold norm_std_window10_a3 > 7.60251e-05
                                        if max_ecross3 < 0.509066:
                                            return 0.0570181
                                        else: #threshold max_ecross3 > 0.509066
                                            if avg_beta23 < 13.6098:
                                                if std_ecross1 < 0.00615182:
                                                    return -0.0101964
                                                else: #threshold std_ecross1 > 0.00615182
                                                    return 0.273125
                                            else: #threshold avg_beta23 > 13.6098
                                                if max_ecross3 < 0.0535005:
                                                    if norm_a2_slope < 2.17222e-10:
                                                        return 0.158093
                                                    else: #threshold norm_a2_slope > 2.17222e-10
                                                        return 0.274184
                                                else: #threshold max_ecross3 > 0.0535005
                                                    if std_ecross2 < 0.00446569:
                                                        if std_ecross1 < 0.00790167:
                                                            return 0.288661
                                                        else: #threshold std_ecross1 > 0.00790167
                                                            if avg_ecross3 < 0.561846:
                                                                if max_beta12 < 16.7283:
                                                                    return -0.0996096
                                                                else: #threshold max_beta12 > 16.7283
                                                                    return -0.34144
                                                            else: #threshold avg_ecross3 > 0.561846
                                                                return 0.243195
                                                    else: #threshold std_ecross2 > 0.00446569
                                                        return 0.140735
                    else: #threshold norm_a3_slope > -8.34671e-11
                        if max_ecross3 < 0.0272602:
                            return 0.084009
                        else: #threshold max_ecross3 > 0.0272602
                            if avg_ecross3 < 0.898338:
                                return 0.28107
                            else: #threshold avg_ecross3 > 0.898338
                                return 0.20413
    #New booster
    if max_ecross2 < 0.51329:
        if std_beta12 < 0.0459785:
            if max_ecross2 < 0.103135:
                return 0.0946914
            else: #threshold max_ecross2 > 0.103135
                return 0.26137
        else: #threshold std_beta12 > 0.0459785
            if avg_beta12 < 5.60667:
                if std_ecross2 < 0.282565:
                    if avg_ecross3 < 0.394874:
                        if norm_max_a1 < 3.03213e-05:
                            if max_ecross2 < 0.174213:
                                return 0.0460721
                            else: #threshold max_ecross2 > 0.174213
                                if avg_beta12 < 5.75024:
                                    if std_beta23 < 0.251725:
                                        if avg_ecross1 < 0.881737:
                                            if norm_max_a2 < 0.000318477:
                                                if std_beta23 < 0.193422:
                                                    return 0.093601
                                                else: #threshold std_beta23 > 0.193422
                                                    if std_ecross2 < 0.0106119:
                                                        if avg_beta23 < 25.4016:
                                                            return 0.181906
                                                        else: #threshold avg_beta23 > 25.4016
                                                            if norm_max_a3 < 3.86941e-05:
                                                                return 0.0896647
                                                            else: #threshold norm_max_a3 > 3.86941e-05
                                                                if norm_max_a2 < 0.00014772:
                                                                    if avg_beta12 < 11.7669:
                                                                        return -0.215813
                                                                    else: #threshold avg_beta12 > 11.7669
                                                                        if max_ecross2 < 0.470648:
                                                                            if std_beta23 < 0.0668833:
                                                                                if min_ecross3 < 0.0975995:
                                                                                    return -0.218676
                                                                                else: #threshold min_ecross3 > 0.0975995
                                                                                    if avg_iH1 < 0.472172:
                                                                                        if norm_max_a2 < 0.00323568:
                                                                                            if norm_a1_slope < -2.83421e-10:
                                                                                                if max_ecross2 < 0.0682702:
                                                                                                    if std_beta12 < 0.0137649:
                                                                                                        return 0.0605399
                                                                                                    else: #threshold std_beta12 > 0.0137649
                                                                                                        return 0.13381
                                                                                                else: #threshold max_ecross2 > 0.0682702
                                                                                                    if std_beta23 < 0.0175755:
                                                                                                        if max_ecross2 < 0.346297:
                                                                                                            return 0.247374
                                                                                                        else: #threshold max_ecross2 > 0.346297
                                                                                                            return 0.0244421
                                                                                                    else: #threshold std_beta23 > 0.0175755
                                                                                                        return 0.247914
                                                                                            else: #threshold norm_a1_slope > -2.83421e-10
                                                                                                return 0.253665
                                                                                        else: #threshold norm_max_a2 > 0.00323568
                                                                                            return -0.207064
                                                                                    else: #threshold avg_iH1 > 0.472172
                                                                                        if avg_beta23 < 7.0018:
                                                                                            return 0.216031
                                                                                        else: #threshold avg_beta23 > 7.0018
                                                                                            if std_ecross2 < 0.0829707:
                                                                                                return 0.138428
                                                                                            else: #threshold std_ecross2 > 0.0829707
                                                                                                if min_ecross1 < 0.0144512:
                                                                                                    return 0.299682
                                                                                                else: #threshold min_ecross1 > 0.0144512
                                                                                                    return -0.127735
                                                                            else: #threshold std_beta23 > 0.0668833
                                                                                if min_ecross2 < 0.041974:
                                                                                    return 0.141548
                                                                                else: #threshold min_ecross2 > 0.041974
                                                                                    if avg_iH1 < 3.03536:
                                                                                        if min_beta12 < 29.0225:
                                                                                            if avg_ecross1 < 0.629936:
                                                                                                if min_ecross2 < 0.0127562:
                                                                                                    return 0.0992865
                                                                                                else: #threshold min_ecross2 > 0.0127562
                                                                                                    return -0.286989
                                                                                            else: #threshold avg_ecross1 > 0.629936
                                                                                                return 0.163085
                                                                                        else: #threshold min_beta12 > 29.0225
                                                                                            if min_ecross1 < 0.361858:
                                                                                                return 0.262398
                                                                                            else: #threshold min_ecross1 > 0.361858
                                                                                                return 0.162322
                                                                                    else: #threshold avg_iH1 > 3.03536
                                                                                        if std_ecross2 < 0.00201382:
                                                                                            return 0.218901
                                                                                        else: #threshold std_ecross2 > 0.00201382
                                                                                            return 0.0140452
                                                                        else: #threshold max_ecross2 > 0.470648
                                                                            if std_ecross2 < 0.0472888:
                                                                                if avg_beta23 < 10.8301:
                                                                                    return -0.0921429
                                                                                else: #threshold avg_beta23 > 10.8301
                                                                                    if avg_ecross3 < 0.425768:
                                                                                        return -0.276645
                                                                                    else: #threshold avg_ecross3 > 0.425768
                                                                                        if std_beta12 < 0.121574:
                                                                                            if max_ecross2 < 0.040196:
                                                                                                return 0.0316054
                                                                                            else: #threshold max_ecross2 > 0.040196
                                                                                                if max_ecross3 < 0.0589487:
                                                                                                    return 0.178241
                                                                                                else: #threshold max_ecross3 > 0.0589487
                                                                                                    return 0.119171
                                                                                        else: #threshold std_beta12 > 0.121574
                                                                                            return 0.25132
                                                                            else: #threshold std_ecross2 > 0.0472888
                                                                                return 0.273676
                                                                else: #threshold norm_max_a2 > 0.00014772
                                                                    if avg_beta23 < 14.8827:
                                                                        if norm_max_window10_a3 < 6.53445e-05:
                                                                            return -0.0638454
                                                                        else: #threshold norm_max_window10_a3 > 6.53445e-05
                                                                            return -0.270419
                                                                    else: #threshold avg_beta23 > 14.8827
                                                                        return 0.301069
                                                    else: #threshold std_ecross2 > 0.0106119
                                                        return -0.239693
                                            else: #threshold norm_max_a2 > 0.000318477
                                                if max_ecross1 < 0.795365:
                                                    return 0.0929452
                                                else: #threshold max_ecross1 > 0.795365
                                                    return -0.162382
                                        else: #threshold avg_ecross1 > 0.881737
                                            if std_beta12 < 0.0302737:
                                                return 0.135786
                                            else: #threshold std_beta12 > 0.0302737
                                                return 0.260138
                                    else: #threshold std_beta23 > 0.251725
                                        if std_ecross2 < 0.139736:
                                            if norm_a3_slope < 1.20554e-10:
                                                if min_ecross1 < 0.238898:
                                                    if max_ecross1 < 0.0412268:
                                                        return 0.152424
                                                    else: #threshold max_ecross1 > 0.0412268
                                                        if min_ecross3 < 0.0434259:
                                                            return -0.0704528
                                                        else: #threshold min_ecross3 > 0.0434259
                                                            if max_ecross2 < 0.525735:
                                                                return 0.265816
                                                            else: #threshold max_ecross2 > 0.525735
                                                                return 0.194739
                                                else: #threshold min_ecross1 > 0.238898
                                                    if norm_max_a2 < 0.00305504:
                                                        if max_ecross2 < 0.624781:
                                                            return 0.267232
                                                        else: #threshold max_ecross2 > 0.624781
                                                            if norm_max_a3 < 0.000145777:
                                                                return -0.182999
                                                            else: #threshold norm_max_a3 > 0.000145777
                                                                return 0.202993
                                                    else: #threshold norm_max_a2 > 0.00305504
                                                        if norm_max_a2 < 0.00175174:
                                                            return 0.266672
                                                        else: #threshold norm_max_a2 > 0.00175174
                                                            return 0.169919
                                            else: #threshold norm_a3_slope > 1.20554e-10
                                                if min_ecross3 < 0.512852:
                                                    if norm_std_window10_a2 < 0.000498274:
                                                        if max_ecross3 < 0.0552433:
                                                            return -0.292219
                                                        else: #threshold max_ecross3 > 0.0552433
                                                            if avg_iH2 < 28.4162:
                                                                if avg_beta23 < 10.0524:
                                                                    return -0.302925
                                                                else: #threshold avg_beta23 > 10.0524
                                                                    return -0.283883
                                                            else: #threshold avg_iH2 > 28.4162
                                                                if norm_std_window10_a2 < 0.000123416:
                                                                    return 0.124192
                                                                else: #threshold norm_std_window10_a2 > 0.000123416
                                                                    return -0.0263312
                                                    else: #threshold norm_std_window10_a2 > 0.000498274
                                                        return 0.253545
                                                else: #threshold min_ecross3 > 0.512852
                                                    return 0.0296614
                                        else: #threshold std_ecross2 > 0.139736
                                            if max_ecross2 < 0.437764:
                                                return 0.0332054
                                            else: #threshold max_ecross2 > 0.437764
                                                if min_beta23 < 6.62198:
                                                    if min_ecross3 < 0.272126:
                                                        if avg_iH2 < 2.58706:
                                                            if norm_a3_slope < 3.04559e-11:
                                                                return 0.165948
                                                            else: #threshold norm_a3_slope > 3.04559e-11
                                                                if avg_iH2 < 0.194056:
                                                                    return -0.0656934
                                                                else: #threshold avg_iH2 > 0.194056
                                                                    return -0.0537395
                                                        else: #threshold avg_iH2 > 2.58706
                                                            return 0.263704
                                                    else: #threshold min_ecross3 > 0.272126
                                                        if max_ecross2 < 0.543638:
                                                            return -0.362101
                                                        else: #threshold max_ecross2 > 0.543638
                                                            if avg_ecross3 < 0.898338:
                                                                return 0.262872
                                                            else: #threshold avg_ecross3 > 0.898338
                                                                if max_ecross2 < 0.0356141:
                                                                    if min_beta23 < 16.9135:
                                                                        if max_ecross3 < 0.002622:
                                                                            return 0.224572
                                                                        else: #threshold max_ecross3 > 0.002622
                                                                            return -0.0350841
                                                                    else: #threshold min_beta23 > 16.9135
                                                                        return 0.169251
                                                                else: #threshold max_ecross2 > 0.0356141
                                                                    if min_beta12 < 22.8193:
                                                                        return 0.150115
                                                                    else: #threshold min_beta12 > 22.8193
                                                                        return -0.223791
                                                else: #threshold min_beta23 > 6.62198
                                                    if std_ecross2 < 0.134973:
                                                        return 0.0721778
                                                    else: #threshold std_ecross2 > 0.134973
                                                        return -0.267726
                                else: #threshold avg_beta12 > 5.75024
                                    if avg_ecross1 < 0.603134:
                                        return 0.220179
                                    else: #threshold avg_ecross1 > 0.603134
                                        return 0.0638813
                        else: #threshold norm_max_a1 > 3.03213e-05
                            if std_ecross2 < 0.0242603:
                                return -0.140261
                            else: #threshold std_ecross2 > 0.0242603
                                return 0.215968
                    else: #threshold avg_ecross3 > 0.394874
                        return 0.164353
                else: #threshold std_ecross2 > 0.282565
                    return 0.256823
            else: #threshold avg_beta12 > 5.60667
                if avg_beta23 < 7.63304:
                    if avg_beta23 < 9.55917:
                        return 0.0938169
                    else: #threshold avg_beta23 > 9.55917
                        return -0.283995
                else: #threshold avg_beta23 > 7.63304
                    return -0.0226714
    else: #threshold max_ecross2 > 0.51329
        if std_beta23 < 0.0204743:
            return -0.090038
        else: #threshold std_beta23 > 0.0204743
            if avg_ecross3 < 1.25248:
                if avg_iH1 < 3.30479:
                    if std_ecross2 < 0.0299057:
                        if max_ecross3 < 0.151142:
                            return 0.208937
                        else: #threshold max_ecross3 > 0.151142
                            if max_ecross2 < 0.196659:
                                return -0.15578
                            else: #threshold max_ecross2 > 0.196659
                                return -0.0252674
                    else: #threshold std_ecross2 > 0.0299057
                        if norm_std_a2 < 0.00127039:
                            if norm_max_window10_a3 < 0.019522:
                                return -0.0897021
                            else: #threshold norm_max_window10_a3 > 0.019522
                                return 0.0864657
                        else: #threshold norm_std_a2 > 0.00127039
                            if avg_iH2 < 4.76588:
                                return -0.238552
                            else: #threshold avg_iH2 > 4.76588
                                return -0.346561
                else: #threshold avg_iH1 > 3.30479
                    return 0.221611
            else: #threshold avg_ecross3 > 1.25248
                if std_beta23 < 0.0114335:
                    if max_ecross2 < 0.228969:
                        return 0.0478492
                    else: #threshold max_ecross2 > 0.228969
                        if max_ecross3 < 0.0973462:
                            if min_ecross2 < 0.0112581:
                                return -0.0812712
                            else: #threshold min_ecross2 > 0.0112581
                                return 0.177487
                        else: #threshold max_ecross3 > 0.0973462
                            if norm_std_window10_a2 < 0.00103759:
                                return 0.253077
                            else: #threshold norm_std_window10_a2 > 0.00103759
                                return 0.131502
                else: #threshold std_beta23 > 0.0114335
                    if norm_max_a1 < 0.0316881:
                        return 0.266804
                    else: #threshold norm_max_a1 > 0.0316881
                        return 0.143323
    #New booster
    if std_beta12 < 0.152237:
        if max_ecross2 < 0.349069:
            if std_beta12 < 0.0232501:
                if avg_ecross3 < 0.432416:
                    return 0.0190396
                else: #threshold avg_ecross3 > 0.432416
                    return -0.315051
            else: #threshold std_beta12 > 0.0232501
                return 0.224358
        else: #threshold max_ecross2 > 0.349069
            if avg_ecross2 < 0.601476:
                if max_ecross1 < 0.171779:
                    if norm_std_a1 < 1.59261e-05:
                        return -0.10051
                    else: #threshold norm_std_a1 > 1.59261e-05
                        return -0.297794
                else: #threshold max_ecross1 > 0.171779
                    return 0.169478
            else: #threshold avg_ecross2 > 0.601476
                if std_ecross3 < 0.0329374:
                    if max_ecross1 < 0.816824:
                        if max_ecross3 < 0.286962:
                            return 0.0557229
                        else: #threshold max_ecross3 > 0.286962
                            if std_beta12 < 0.0353347:
                                return -0.0345455
                            else: #threshold std_beta12 > 0.0353347
                                return -0.0587095
                    else: #threshold max_ecross1 > 0.816824
                        if max_beta23 < 19.9168:
                            if std_beta23 < 0.181644:
                                if min_ecross1 < 0.362653:
                                    return 0.242151
                                else: #threshold min_ecross1 > 0.362653
                                    return 0.160919
                            else: #threshold std_beta23 > 0.181644
                                if std_ecross3 < 0.030786:
                                    if avg_iH1 < 3.22218:
                                        return 0.170902
                                    else: #threshold avg_iH1 > 3.22218
                                        return 0.2491
                                else: #threshold std_ecross3 > 0.030786
                                    if std_ecross2 < 0.0733621:
                                        return -0.286632
                                    else: #threshold std_ecross2 > 0.0733621
                                        return 0.0846348
                        else: #threshold max_beta23 > 19.9168
                            if avg_ecross2 < 0.27467:
                                if avg_beta12 < 11.8365:
                                    if norm_a1_slope < -1.3124e-10:
                                        if min_ecross1 < 0.401244:
                                            return 0.0425158
                                        else: #threshold min_ecross1 > 0.401244
                                            if min_beta23 < 15.5838:
                                                return 0.0813284
                                            else: #threshold min_beta23 > 15.5838
                                                if norm_a2_slope < -1.55888e-11:
                                                    if max_beta23 < 24.1983:
                                                        if norm_std_a3 < 5.232e-05:
                                                            if norm_std_a2 < 5.43519e-05:
                                                                return 0.20144
                                                            else: #threshold norm_std_a2 > 5.43519e-05
                                                                return 0.254031
                                                        else: #threshold norm_std_a3 > 5.232e-05
                                                            return 0.190172
                                                    else: #threshold max_beta23 > 24.1983
                                                        return 0.255883
                                                else: #threshold norm_a2_slope > -1.55888e-11
                                                    if norm_max_window10_a2 < 0.00058811:
                                                        return -0.199822
                                                    else: #threshold norm_max_window10_a2 > 0.00058811
                                                        if std_beta12 < 0.0936375:
                                                            return 0.249265
                                                        else: #threshold std_beta12 > 0.0936375
                                                            return 0.123319
                                    else: #threshold norm_a1_slope > -1.3124e-10
                                        return -0.00527654
                                else: #threshold avg_beta12 > 11.8365
                                    if avg_iH1 < 0.445481:
                                        if std_ecross2 < 0.0559571:
                                            return 0.139807
                                        else: #threshold std_ecross2 > 0.0559571
                                            return 0.233069
                                    else: #threshold avg_iH1 > 0.445481
                                        if avg_beta12 < 4.66351:
                                            if max_ecross2 < 0.172063:
                                                if norm_std_window10_a3 < 5.19171e-05:
                                                    if norm_a1_slope < 1.5362e-10:
                                                        return 0.203426
                                                    else: #threshold norm_a1_slope > 1.5362e-10
                                                        return 0.017401
                                                else: #threshold norm_std_window10_a3 > 5.19171e-05
                                                    if std_ecross3 < 0.0580956:
                                                        return -0.165402
                                                    else: #threshold std_ecross3 > 0.0580956
                                                        return 0.169349
                                            else: #threshold max_ecross2 > 0.172063
                                                return -0.307393
                                        else: #threshold avg_beta12 > 4.66351
                                            return 0.244745
                            else: #threshold avg_ecross2 > 0.27467
                                return 0.0812909
                else: #threshold std_ecross3 > 0.0329374
                    if norm_std_window10_a1 < 0.00186678:
                        if norm_a2_slope < -2.39947e-11:
                            return 0.0967712
                        else: #threshold norm_a2_slope > -2.39947e-11
                            return 0.183624
                    else: #threshold norm_std_window10_a1 > 0.00186678
                        return 0.148467
    else: #threshold std_beta12 > 0.152237
        if std_beta23 < 0.0204731:
            return 0.251025
        else: #threshold std_beta23 > 0.0204731
            return 0.133931
    #New booster
    if norm_max_a2 < 0.00331094:
        if max_ecross2 < 0.344123:
            if std_beta12 < 0.0267032:
                if avg_ecross1 < 0.187796:
                    if min_ecross1 < 0.255691:
                        if norm_max_a3 < 0.000831872:
                            if avg_ecross1 < 0.0170529:
                                if max_ecross2 < 0.444958:
                                    if max_ecross1 < 0.233963:
                                        if avg_ecross3 < 0.053621:
                                            if norm_max_window10_a1 < 5.61472e-05:
                                                return 0.103329
                                            else: #threshold norm_max_window10_a1 > 5.61472e-05
                                                return 0.215524
                                        else: #threshold avg_ecross3 > 0.053621
                                            return -0.19985
                                    else: #threshold max_ecross1 > 0.233963
                                        return -0.0259366
                                else: #threshold max_ecross2 > 0.444958
                                    if avg_beta12 < 6.73915:
                                        if max_ecross1 < 0.349672:
                                            return -0.339422
                                        else: #threshold max_ecross1 > 0.349672
                                            return 0.0613845
                                    else: #threshold avg_beta12 > 6.73915
                                        if avg_iH1 < 0.0859361:
                                            return 0.0825026
                                        else: #threshold avg_iH1 > 0.0859361
                                            if norm_std_a1 < 0.000257043:
                                                if min_beta23 < 8.17781:
                                                    return 0.0318905
                                                else: #threshold min_beta23 > 8.17781
                                                    return -0.302791
                                            else: #threshold norm_std_a1 > 0.000257043
                                                return 0.150086
                            else: #threshold avg_ecross1 > 0.0170529
                                return -0.25299
                        else: #threshold norm_max_a3 > 0.000831872
                            return 0.137405
                    else: #threshold min_ecross1 > 0.255691
                        if norm_std_a2 < 0.00013774:
                            return -0.253474
                        else: #threshold norm_std_a2 > 0.00013774
                            if max_ecross2 < 0.328005:
                                if max_ecross2 < 0.0851391:
                                    return 0.0421554
                                else: #threshold max_ecross2 > 0.0851391
                                    if avg_beta23 < 8.0165:
                                        return 0.135879
                                    else: #threshold avg_beta23 > 8.0165
                                        return -0.256144
                            else: #threshold max_ecross2 > 0.328005
                                if avg_ecross1 < 0.894715:
                                    if avg_beta12 < 9.98286:
                                        if norm_max_a3 < 8.35042e-05:
                                            return 0.154659
                                        else: #threshold norm_max_a3 > 8.35042e-05
                                            return 0.239923
                                    else: #threshold avg_beta12 > 9.98286
                                        return 0.242145
                                else: #threshold avg_ecross1 > 0.894715
                                    return 0.098966
                else: #threshold avg_ecross1 > 0.187796
                    if min_ecross3 < 0.309152:
                        return -0.154224
                    else: #threshold min_ecross3 > 0.309152
                        if max_ecross2 < 0.180563:
                            if max_ecross3 < 0.0109332:
                                return 0.122969
                            else: #threshold max_ecross3 > 0.0109332
                                return -0.292408
                        else: #threshold max_ecross2 > 0.180563
                            return 0.163645
            else: #threshold std_beta12 > 0.0267032
                if norm_max_window10_a2 < 5.17823e-05:
                    return 0.0422198
                else: #threshold norm_max_window10_a2 > 5.17823e-05
                    return -0.156022
        else: #threshold max_ecross2 > 0.344123
            if avg_ecross2 < 0.601476:
                if max_ecross2 < 0.194813:
                    return -0.0398769
                else: #threshold max_ecross2 > 0.194813
                    return -0.252116
            else: #threshold avg_ecross2 > 0.601476
                if avg_ecross1 < 0.00682385:
                    return 0.228118
                else: #threshold avg_ecross1 > 0.00682385
                    return 0.00471644
    else: #threshold norm_max_a2 > 0.00331094
        if std_beta23 < 0.0205437:
            if std_ecross2 < 0.253667:
                return -0.169825
            else: #threshold std_ecross2 > 0.253667
                if avg_ecross3 < 0.898663:
                    return 0.0863848
                else: #threshold avg_ecross3 > 0.898663
                    return 0.211734
        else: #threshold std_beta23 > 0.0205437
            return 0.238509
    #New booster
    if std_beta12 < 0.168647:
        if max_ecross2 < 0.230246:
            if avg_ecross3 < 0.652476:
                return 0.229437
            else: #threshold avg_ecross3 > 0.652476
                return 0.142692
        else: #threshold max_ecross2 > 0.230246
            if max_ecross2 < 0.0866173:
                if avg_ecross3 < 0.465251:
                    if min_ecross3 < 0.134857:
                        if min_beta12 < 19.169:
                            if max_ecross1 < 0.127781:
                                return 0.0885
                            else: #threshold max_ecross1 > 0.127781
                                if norm_max_a1 < 0.000110563:
                                    if norm_std_window10_a1 < 0.00010968:
                                        if std_ecross3 < 0.00574754:
                                            return -0.0868046
                                        else: #threshold std_ecross3 > 0.00574754
                                            return 0.172958
                                    else: #threshold norm_std_window10_a1 > 0.00010968
                                        return -0.0443765
                                else: #threshold norm_max_a1 > 0.000110563
                                    if norm_a1_slope < -5.56948e-13:
                                        return 0.187411
                                    else: #threshold norm_a1_slope > -5.56948e-13
                                        return 0.0208884
                        else: #threshold min_beta12 > 19.169
                            return 0.227731
                    else: #threshold min_ecross3 > 0.134857
                        return 0.253243
                else: #threshold avg_ecross3 > 0.465251
                    if max_beta12 < 23.6437:
                        return 0.157997
                    else: #threshold max_beta12 > 23.6437
                        return -0.0395085
            else: #threshold max_ecross2 > 0.0866173
                if max_ecross1 < 0.0789659:
                    return -0.0364911
                else: #threshold max_ecross1 > 0.0789659
                    return -0.139861
    else: #threshold std_beta12 > 0.168647
        if std_beta12 < 0.0158006:
            if std_ecross2 < 0.24789:
                if avg_iH2 < 4.37451:
                    return 0.0341425
                else: #threshold avg_iH2 > 4.37451
                    return -0.0206058
            else: #threshold std_ecross2 > 0.24789
                if max_ecross2 < 0.156861:
                    return 0.176377
                else: #threshold max_ecross2 > 0.156861
                    return -0.246044
        else: #threshold std_beta12 > 0.0158006
            if norm_a3_slope < 4.67736e-10:
                return 0.15315
            else: #threshold norm_a3_slope > 4.67736e-10
                return 0.219932
    #New booster
    if norm_max_a2 < 0.00346695:
        if std_beta23 < 0.0199795:
            if max_ecross2 < 0.230296:
                if min_ecross1 < 0.305723:
                    return 0.216477
                else: #threshold min_ecross1 > 0.305723
                    return 0.120642
            else: #threshold max_ecross2 > 0.230296
                if min_beta23 < 7.55917:
                    if norm_max_a2 < 7.9986e-05:
                        if max_ecross3 < 0.237378:
                            if min_beta12 < 17.9266:
                                return -0.0878317
                            else: #threshold min_beta12 > 17.9266
                                if avg_ecross1 < 0.0642498:
                                    if std_ecross3 < 0.00842768:
                                        return 0.201742
                                    else: #threshold std_ecross3 > 0.00842768
                                        return 0.0503566
                                else: #threshold avg_ecross1 > 0.0642498
                                    if min_ecross1 < 0.000680189:
                                        return 0.108251
                                    else: #threshold min_ecross1 > 0.000680189
                                        return -0.267622
                        else: #threshold max_ecross3 > 0.237378
                            if std_beta12 < 0.0201604:
                                if norm_max_window10_a3 < 0.00553439:
                                    return 0.13575
                                else: #threshold norm_max_window10_a3 > 0.00553439
                                    return 0.281458
                            else: #threshold std_beta12 > 0.0201604
                                return -0.197263
                    else: #threshold norm_max_a2 > 7.9986e-05
                        if min_beta23 < 15.7049:
                            if max_ecross2 < 0.17528:
                                if avg_iH1 < 4.66851:
                                    return 0.212199
                                else: #threshold avg_iH1 > 4.66851
                                    if norm_a1_slope < 3.44395e-10:
                                        if min_ecross3 < 0.530004:
                                            return 0.072957
                                        else: #threshold min_ecross3 > 0.530004
                                            return -0.194091
                                    else: #threshold norm_a1_slope > 3.44395e-10
                                        if max_beta23 < 6.58899:
                                            if avg_ecross1 < 0.0326117:
                                                return 0.033613
                                            else: #threshold avg_ecross1 > 0.0326117
                                                if norm_a1_slope < 1.3158e-12:
                                                    return 0.0413074
                                                else: #threshold norm_a1_slope > 1.3158e-12
                                                    if max_ecross2 < 0.521236:
                                                        return 0.0719966
                                                    else: #threshold max_ecross2 > 0.521236
                                                        if std_ecross3 < 0.0457328:
                                                            if avg_iH2 < 1.09844:
                                                                if avg_ecross2 < 0.258105:
                                                                    if norm_std_window10_a3 < 4.6413e-06:
                                                                        if min_beta12 < 19.8296:
                                                                            if norm_max_a2 < 0.000233613:
                                                                                return 0.215733
                                                                            else: #threshold norm_max_a2 > 0.000233613
                                                                                return 0.133783
                                                                        else: #threshold min_beta12 > 19.8296
                                                                            if std_ecross2 < 0.00467424:
                                                                                if avg_ecross1 < 0.142636:
                                                                                    return -0.0864006
                                                                                else: #threshold avg_ecross1 > 0.142636
                                                                                    if std_ecross2 < 0.00449082:
                                                                                        return -0.21958
                                                                                    else: #threshold std_ecross2 > 0.00449082
                                                                                        if avg_iH1 < 2.83353:
                                                                                            if max_ecross2 < 0.264791:
                                                                                                return -0.265569
                                                                                            else: #threshold max_ecross2 > 0.264791
                                                                                                return -0.0729159
                                                                                        else: #threshold avg_iH1 > 2.83353
                                                                                            return 0.227135
                                                                            else: #threshold std_ecross2 > 0.00467424
                                                                                return 0.0312084
                                                                    else: #threshold norm_std_window10_a3 > 4.6413e-06
                                                                        return -0.144229
                                                                else: #threshold avg_ecross2 > 0.258105
                                                                    return -0.0334469
                                                            else: #threshold avg_iH2 > 1.09844
                                                                if std_beta23 < 0.0156871:
                                                                    return -0.215166
                                                                else: #threshold std_beta23 > 0.0156871
                                                                    return -0.250003
                                                        else: #threshold std_ecross3 > 0.0457328
                                                            if min_beta23 < 25.8146:
                                                                if norm_std_window10_a3 < 1.99869e-05:
                                                                    if min_beta12 < 9.43604:
                                                                        return -0.29486
                                                                    else: #threshold min_beta12 > 9.43604
                                                                        if max_beta23 < 15.7046:
                                                                            return 0.128017
                                                                        else: #threshold max_beta23 > 15.7046
                                                                            return -0.172756
                                                                else: #threshold norm_std_window10_a3 > 1.99869e-05
                                                                    if avg_ecross3 < 0.0414967:
                                                                        if max_beta12 < 24.2073:
                                                                            if norm_a1_slope < -7.64018e-12:
                                                                                if norm_a1_slope < 1.32856e-12:
                                                                                    if norm_max_a3 < 0.000111693:
                                                                                        return 0.139809
                                                                                    else: #threshold norm_max_a3 > 0.000111693
                                                                                        return 0.222677
                                                                                else: #threshold norm_a1_slope > 1.32856e-12
                                                                                    return 0.0107967
                                                                            else: #threshold norm_a1_slope > -7.64018e-12
                                                                                return 0.210493
                                                                        else: #threshold max_beta12 > 24.2073
                                                                            return 0.078646
                                                                    else: #threshold avg_ecross3 > 0.0414967
                                                                        if avg_iH2 < 3.08038:
                                                                            return -0.263954
                                                                        else: #threshold avg_iH2 > 3.08038
                                                                            return 0.108335
                                                            else: #threshold min_beta23 > 25.8146
                                                                return 0.0596533
                                        else: #threshold max_beta23 > 6.58899
                                            if std_beta23 < 0.145512:
                                                if min_ecross2 < 0.125604:
                                                    if max_ecross2 < 0.290133:
                                                        return 0.222615
                                                    else: #threshold max_ecross2 > 0.290133
                                                        return 0.14017
                                                else: #threshold min_ecross2 > 0.125604
                                                    if avg_ecross2 < 0.613531:
                                                        if max_ecross3 < 0.289999:
                                                            if norm_max_a3 < 0.0126999:
                                                                if min_ecross3 < 0.290903:
                                                                    if min_beta23 < 13.1898:
                                                                        return 0.229675
                                                                    else: #threshold min_beta23 > 13.1898
                                                                        return 0.126086
                                                                else: #threshold min_ecross3 > 0.290903
                                                                    if norm_max_a3 < 3.30121e-05:
                                                                        if max_ecross2 < 0.458274:
                                                                            if avg_ecross3 < 0.0839507:
                                                                                if max_ecross3 < 0.046631:
                                                                                    if avg_ecross1 < 0.288635:
                                                                                        if min_ecross1 < 0.393974:
                                                                                            return 0.0918473
                                                                                        else: #threshold min_ecross1 > 0.393974
                                                                                            if norm_max_a2 < 0.000380064:
                                                                                                return -0.069654
                                                                                            else: #threshold norm_max_a2 > 0.000380064
                                                                                                return -0.0150611
                                                                                    else: #threshold avg_ecross1 > 0.288635
                                                                                        return -0.0528786
                                                                                else: #threshold max_ecross3 > 0.046631
                                                                                    return 0.209449
                                                                            else: #threshold avg_ecross3 > 0.0839507
                                                                                if avg_ecross1 < 0.0502172:
                                                                                    if norm_a3_slope < -4.65367e-13:
                                                                                        return -0.0461297
                                                                                    else: #threshold norm_a3_slope > -4.65367e-13
                                                                                        if max_ecross3 < 0.0436695:
                                                                                            if norm_a3_slope < -1.34161e-11:
                                                                                                return -0.136074
                                                                                            else: #threshold norm_a3_slope > -1.34161e-11
                                                                                                if min_ecross1 < 0.411353:
                                                                                                    return 0.125591
                                                                                                else: #threshold min_ecross1 > 0.411353
                                                                                                    if min_beta12 < 22.6917:
                                                                                                        return -0.15579
                                                                                                    else: #threshold min_beta12 > 22.6917
                                                                                                        if min_ecross1 < 0.0744615:
                                                                                                            if min_ecross1 < 0.0565017:
                                                                                                                if min_beta23 < 11.5061:
                                                                                                                    return -0.206929
                                                                                                                else: #threshold min_beta23 > 11.5061
                                                                                                                    if max_ecross2 < 0.665929:
                                                                                                                        return 0.223654
                                                                                                                    else: #threshold max_ecross2 > 0.665929
                                                                                                                        if avg_iH2 < 1.69921:
                                                                                                                            if norm_a1_slope < -8.30105e-11:
                                                                                                                                if min_ecross1 < 0.707596:
                                                                                                                                    if avg_ecross2 < 0.376063:
                                                                                                                                        if norm_a2_slope < 9.6514e-11:
                                                                                                                                            return 0.215289
                                                                                                                                        else: #threshold norm_a2_slope > 9.6514e-11
                                                                                                                                            return 0.148185
                                                                                                                                    else: #threshold avg_ecross2 > 0.376063
                                                                                                                                        if norm_a2_slope < -1.83016e-10:
                                                                                                                                            if avg_iH2 < 0.674897:
                                                                                                                                                return -0.0723182
                                                                                                                                            else: #threshold avg_iH2 > 0.674897
                                                                                                                                                if std_beta12 < 0.063931:
                                                                                                                                                    return -0.0724679
                                                                                                                                                else: #threshold std_beta12 > 0.063931
                                                                                                                                                    if norm_std_a2 < 6.07174e-05:
                                                                                                                                                        if min_ecross1 < 0.31063:
                                                                                                                                                            return 0.206017
                                                                                                                                                        else: #threshold min_ecross1 > 0.31063
                                                                                                                                                            if max_ecross2 < 0.153656:
                                                                                                                                                                return -0.283263
                                                                                                                                                            else: #threshold max_ecross2 > 0.153656
                                                                                                                                                                if avg_ecross1 < 0.171342:
                                                                                                                                                                    if norm_a2_slope < 8.6495e-13:
                                                                                                                                                                        return 0.210875
                                                                                                                                                                    else: #threshold norm_a2_slope > 8.6495e-13
                                                                                                                                                                        if min_ecross1 < 0.14599:
                                                                                                                                                                            return 0.0769322
                                                                                                                                                                        else: #threshold min_ecross1 > 0.14599
                                                                                                                                                                            return 0.240554
                                                                                                                                                                else: #threshold avg_ecross1 > 0.171342
                                                                                                                                                                    return -0.341048
                                                                                                                                                    else: #threshold norm_std_a2 > 6.07174e-05
                                                                                                                                                        if std_ecross2 < 0.0364966:
                                                                                                                                                            if avg_iH1 < 0.48319:
                                                                                                                                                                return 0.0979957
                                                                                                                                                            else: #threshold avg_iH1 > 0.48319
                                                                                                                                                                if max_beta23 < 7.03424:
                                                                                                                                                                    if avg_iH1 < 4.09742:
                                                                                                                                                                        return 0.107708
                                                                                                                                                                    else: #threshold avg_iH1 > 4.09742
                                                                                                                                                                        return 0.220152
                                                                                                                                                                else: #threshold max_beta23 > 7.03424
                                                                                                                                                                    if min_beta23 < 24.6008:
                                                                                                                                                                        return 0.171955
                                                                                                                                                                    else: #threshold min_beta23 > 24.6008
                                                                                                                                                                        if norm_a3_slope < 2.06512e-11:
                                                                                                                                                                            return 0.213881
                                                                                                                                                                        else: #threshold norm_a3_slope > 2.06512e-11
                                                                                                                                                                            return 0.0418612
                                                                                                                                                        else: #threshold std_ecross2 > 0.0364966
                                                                                                                                                            if min_beta12 < 25.4029:
                                                                                                                                                                return -0.113971
                                                                                                                                                            else: #threshold min_beta12 > 25.4029
                                                                                                                                                                return 0.172634
                                                                                                                                        else: #threshold norm_a2_slope > -1.83016e-10
                                                                                                                                            return 0.193872
                                                                                                                                else: #threshold min_ecross1 > 0.707596
                                                                                                                                    if avg_ecross1 < 0.277851:
                                                                                                                                        if min_ecross1 < 0.00256799:
                                                                                                                                            return 0.0266959
                                                                                                                                        else: #threshold min_ecross1 > 0.00256799
                                                                                                                                            if avg_ecross2 < 0.807213:
                                                                                                                                                return 0.116829
                                                                                                                                            else: #threshold avg_ecross2 > 0.807213
                                                                                                                                                if avg_ecross2 < 0.899486:
                                                                                                                                                    if max_ecross3 < 0.0619074:
                                                                                                                                                        return -0.101429
                                                                                                                                                    else: #threshold max_ecross3 > 0.0619074
                                                                                                                                                        return 0.15338
                                                                                                                                                else: #threshold avg_ecross2 > 0.899486
                                                                                                                                                    if max_beta12 < 13.1695:
                                                                                                                                                        return -0.114633
                                                                                                                                                    else: #threshold max_beta12 > 13.1695
                                                                                                                                                        return -0.240254
                                                                                                                                    else: #threshold avg_ecross1 > 0.277851
                                                                                                                                        if std_ecross1 < 0.00522249:
                                                                                                                                            return -0.058905
                                                                                                                                        else: #threshold std_ecross1 > 0.00522249
                                                                                                                                            if norm_a3_slope < -7.44775e-12:
                                                                                                                                                return -0.359829
                                                                                                                                            else: #threshold norm_a3_slope > -7.44775e-12
                                                                                                                                                if avg_iH1 < 1.55005:
                                                                                                                                                    return 0.146618
                                                                                                                                                else: #threshold avg_iH1 > 1.55005
                                                                                                                                                    return -0.0292501
                                                                                                                            else: #threshold norm_a1_slope > -8.30105e-11
                                                                                                                                if avg_ecross1 < 0.188878:
                                                                                                                                    if min_beta12 < 4.76328:
                                                                                                                                        if min_ecross2 < 0.0138941:
                                                                                                                                            if max_ecross3 < 0.125205:
                                                                                                                                                if avg_ecross2 < 0.268307:
                                                                                                                                                    return 0.0974861
                                                                                                                                                else: #threshold avg_ecross2 > 0.268307
                                                                                                                                                    return -0.315151
                                                                                                                                            else: #threshold max_ecross3 > 0.125205
                                                                                                                                                return 0.219627
                                                                                                                                        else: #threshold min_ecross2 > 0.0138941
                                                                                                                                            if std_ecross3 < 0.129438:
                                                                                                                                                if norm_a1_slope < -1.28913e-10:
                                                                                                                                                    return 0.188737
                                                                                                                                                else: #threshold norm_a1_slope > -1.28913e-10
                                                                                                                                                    return -0.00418448
                                                                                                                                            else: #threshold std_ecross3 > 0.129438
                                                                                                                                                return -0.0984068
                                                                                                                                    else: #threshold min_beta12 > 4.76328
                                                                                                                                        return 0.232035
                                                                                                                                else: #threshold avg_ecross1 > 0.188878
                                                                                                                                    return -0.139742
                                                                                                                        else: #threshold avg_iH2 > 1.69921
                                                                                                                            if min_beta12 < 18.5891:
                                                                                                                                if min_ecross1 < 0.00710332:
                                                                                                                                    return 0.140134
                                                                                                                                else: #threshold min_ecross1 > 0.00710332
                                                                                                                                    if std_beta23 < 0.129462:
                                                                                                                                        return 0.127078
                                                                                                                                    else: #threshold std_beta23 > 0.129462
                                                                                                                                        return -0.0475318
                                                                                                                            else: #threshold min_beta12 > 18.5891
                                                                                                                                return 0.213519
                                                                                                            else: #threshold min_ecross1 > 0.0565017
                                                                                                                return 0.101822
                                                                                                        else: #threshold min_ecross1 > 0.0744615
                                                                                                            if max_ecross3 < 0.0401061:
                                                                                                                if std_beta12 < 0.00887388:
                                                                                                                    return -0.0674185
                                                                                                                else: #threshold std_beta12 > 0.00887388
                                                                                                                    return -0.224058
                                                                                                            else: #threshold max_ecross3 > 0.0401061
                                                                                                                if std_ecross2 < 0.0151779:
                                                                                                                    if min_ecross2 < 0.0538487:
                                                                                                                        return 0.101262
                                                                                                                    else: #threshold min_ecross2 > 0.0538487
                                                                                                                        return 0.0171273
                                                                                                                else: #threshold std_ecross2 > 0.0151779
                                                                                                                    return -0.109706
                                                                                        else: #threshold max_ecross3 > 0.0436695
                                                                                            if max_ecross3 < 0.122505:
                                                                                                if norm_std_a2 < 0.00139004:
                                                                                                    return 0.210359
                                                                                                else: #threshold norm_std_a2 > 0.00139004
                                                                                                    return 0.0762478
                                                                                            else: #threshold max_ecross3 > 0.122505
                                                                                                if avg_ecross3 < 1.32255:
                                                                                                    if avg_ecross3 < 0.182244:
                                                                                                        return 0.136439
                                                                                                    else: #threshold avg_ecross3 > 0.182244
                                                                                                        return -0.1381
                                                                                                else: #threshold avg_ecross3 > 1.32255
                                                                                                    return 0.206811
                                                                                else: #threshold avg_ecross1 > 0.0502172
                                                                                    return 0.0662473
                                                                        else: #threshold max_ecross2 > 0.458274
                                                                            return -0.0134569
                                                                    else: #threshold norm_max_a3 > 3.30121e-05
                                                                        if avg_iH1 < 0.733868:
                                                                            return 0.167783
                                                                        else: #threshold avg_iH1 > 0.733868
                                                                            return 0.102739
                                                            else: #threshold norm_max_a3 > 0.0126999
                                                                if std_ecross3 < 0.0647564:
                                                                    if std_ecross1 < 0.0062538:
                                                                        if avg_ecross3 < 0.560554:
                                                                            return 0.056298
                                                                        else: #threshold avg_ecross3 > 0.560554
                                                                            return -0.301208
                                                                    else: #threshold std_ecross1 > 0.0062538
                                                                        if min_beta12 < 6.86726:
                                                                            if min_beta12 < 23.2877:
                                                                                return 0.0135668
                                                                            else: #threshold min_beta12 > 23.2877
                                                                                return -0.193716
                                                                        else: #threshold min_beta12 > 6.86726
                                                                            return -0.023371
                                                                else: #threshold std_ecross3 > 0.0647564
                                                                    return 0.232857
                                                        else: #threshold max_ecross3 > 0.289999
                                                            if norm_max_a3 < 0.000513993:
                                                                return -0.016181
                                                            else: #threshold norm_max_a3 > 0.000513993
                                                                if std_beta23 < 0.229651:
                                                                    if max_ecross2 < 0.0851391:
                                                                        return 0.213675
                                                                    else: #threshold max_ecross2 > 0.0851391
                                                                        return 0.12831
                                                                else: #threshold std_beta23 > 0.229651
                                                                    if avg_ecross1 < 0.894715:
                                                                        return 0.0151945
                                                                    else: #threshold avg_ecross1 > 0.894715
                                                                        if min_ecross1 < 0.247582:
                                                                            return 0.18664
                                                                        else: #threshold min_ecross1 > 0.247582
                                                                            if max_beta23 < 9.3801:
                                                                                return -0.298966
                                                                            else: #threshold max_beta23 > 9.3801
                                                                                return -0.253192
                                                    else: #threshold avg_ecross2 > 0.613531
                                                        if norm_a1_slope < 3.48731e-11:
                                                            if norm_max_window10_a2 < 8.81209e-05:
                                                                if min_ecross2 < 0.00336381:
                                                                    return -0.130311
                                                                else: #threshold min_ecross2 > 0.00336381
                                                                    if norm_std_window10_a3 < 0.000966805:
                                                                        if avg_ecross2 < 1.16117:
                                                                            if std_ecross2 < 0.121735:
                                                                                return 0.15294
                                                                            else: #threshold std_ecross2 > 0.121735
                                                                                return 0.00681068
                                                                        else: #threshold avg_ecross2 > 1.16117
                                                                            if min_ecross1 < 0.486989:
                                                                                if min_beta12 < 10.8834:
                                                                                    if max_ecross2 < 0.110572:
                                                                                        if min_beta12 < 16.2605:
                                                                                            return 0.0204787
                                                                                        else: #threshold min_beta12 > 16.2605
                                                                                            if min_ecross2 < 0.465201:
                                                                                                return -0.155814
                                                                                            else: #threshold min_ecross2 > 0.465201
                                                                                                return -0.225431
                                                                                    else: #threshold max_ecross2 > 0.110572
                                                                                        if max_ecross2 < 0.0983645:
                                                                                            if max_ecross2 < 0.269435:
                                                                                                if min_ecross3 < 0.00693712:
                                                                                                    return 0.185725
                                                                                                else: #threshold min_ecross3 > 0.00693712
                                                                                                    return 0.0279642
                                                                                            else: #threshold max_ecross2 > 0.269435
                                                                                                if std_beta12 < 0.00995792:
                                                                                                    return -0.305799
                                                                                                else: #threshold std_beta12 > 0.00995792
                                                                                                    if avg_ecross1 < 0.536425:
                                                                                                        return 0.0901611
                                                                                                    else: #threshold avg_ecross1 > 0.536425
                                                                                                        return 0.0547833
                                                                                        else: #threshold max_ecross2 > 0.0983645
                                                                                            return 0.146168
                                                                                else: #threshold min_beta12 > 10.8834
                                                                                    if norm_std_a2 < 0.000434624:
                                                                                        if min_ecross1 < 0.0792644:
                                                                                            return -0.232603
                                                                                        else: #threshold min_ecross1 > 0.0792644
                                                                                            if max_ecross3 < 0.00451872:
                                                                                                return 0.207001
                                                                                            else: #threshold max_ecross3 > 0.00451872
                                                                                                return 0.136461
                                                                                    else: #threshold norm_std_a2 > 0.000434624
                                                                                        return 0.188146
                                                                            else: #threshold min_ecross1 > 0.486989
                                                                                if min_ecross1 < 0.00383697:
                                                                                    return 0.1884
                                                                                else: #threshold min_ecross1 > 0.00383697
                                                                                    return -0.0953739
                                                                    else: #threshold norm_std_window10_a3 > 0.000966805
                                                                        if norm_a2_slope < 6.8798e-12:
                                                                            return 0.00811166
                                                                        else: #threshold norm_a2_slope > 6.8798e-12
                                                                            return 0.199236
                                                            else: #threshold norm_max_window10_a2 > 8.81209e-05
                                                                return -0.083951
                                                        else: #threshold norm_a1_slope > 3.48731e-11
                                                            return 0.210625
                                            else: #threshold std_beta23 > 0.145512
                                                return -0.128792
                            else: #threshold max_ecross2 > 0.17528
                                return -0.24887
                        else: #threshold min_beta23 > 15.7049
                            if avg_ecross2 < 0.290119:
                                return 0.100815
                            else: #threshold avg_ecross2 > 0.290119
                                return 0.254094
                else: #threshold min_beta23 > 7.55917
                    return 0.194928
        else: #threshold std_beta23 > 0.0199795
            if avg_ecross2 < 0.757183:
                return 0.216012
            else: #threshold avg_ecross2 > 0.757183
                return 0.158488
    else: #threshold norm_max_a2 > 0.00346695
        if std_beta12 < 0.0148759:
            if std_ecross2 < 0.168489:
                return 0.144619
            else: #threshold std_ecross2 > 0.168489
                return 0.0507098
        else: #threshold std_beta12 > 0.0148759
            if std_ecross3 < 0.281099:
                if min_ecross3 < 0.000261938:
                    if avg_ecross3 < 0.526704:
                        return 0.208714
                    else: #threshold avg_ecross3 > 0.526704
                        return -0.0102028
                else: #threshold min_ecross3 > 0.000261938
                    if min_beta23 < 24.256:
                        if avg_ecross1 < 0.937942:
                            if min_beta23 < 14.5251:
                                if norm_std_a2 < 2.48506e-05:
                                    if max_ecross2 < 0.319603:
                                        return 0.233977
                                    else: #threshold max_ecross2 > 0.319603
                                        return 0.0475356
                                else: #threshold norm_std_a2 > 2.48506e-05
                                    return 0.201884
                            else: #threshold min_beta23 > 14.5251
                                return 0.209374
                        else: #threshold avg_ecross1 > 0.937942
                            return 0.149265
                    else: #threshold min_beta23 > 24.256
                        if max_ecross2 < 0.112253:
                            if min_ecross2 < 0.00199404:
                                return 0.0726388
                            else: #threshold min_ecross2 > 0.00199404
                                if norm_std_a3 < 3.93375e-05:
                                    return 0.137522
                                else: #threshold norm_std_a3 > 3.93375e-05
                                    return 0.211934
                        else: #threshold max_ecross2 > 0.112253
                            return -0.0734764
            else: #threshold std_ecross3 > 0.281099
                return 0.10815
    #New booster
    if max_ecross2 < 0.490431:
        if std_beta23 < 0.0242839:
            if avg_ecross2 < 0.469782:
                if max_beta12 < 22.0859:
                    if min_beta12 < 9.80709:
                        if avg_beta23 < 9.97381:
                            return -0.0301293
                        else: #threshold avg_beta23 > 9.97381
                            return -0.273093
                    else: #threshold min_beta12 > 9.80709
                        return -0.0554273
                else: #threshold max_beta12 > 22.0859
                    return -0.321171
            else: #threshold avg_ecross2 > 0.469782
                return 0.016439
        else: #threshold std_beta23 > 0.0242839
            if max_ecross2 < 0.173472:
                return 0.115311
            else: #threshold max_ecross2 > 0.173472
                if avg_beta23 < 10.4873:
                    return 0.175166
                else: #threshold avg_beta23 > 10.4873
                    if max_ecross2 < 0.291424:
                        if avg_ecross1 < 0.36908:
                            return 0.0189073
                        else: #threshold avg_ecross1 > 0.36908
                            return 0.161912
                    else: #threshold max_ecross2 > 0.291424
                        if max_ecross1 < 0.537614:
                            return 0.136377
                        else: #threshold max_ecross1 > 0.537614
                            if avg_beta12 < 6.72902:
                                return -0.0618939
                            else: #threshold avg_beta12 > 6.72902
                                if norm_max_a1 < 0.0033346:
                                    return 0.150377
                                else: #threshold norm_max_a1 > 0.0033346
                                    if norm_max_a2 < 0.000243611:
                                        if norm_max_a2 < 0.00122182:
                                            return 0.011423
                                        else: #threshold norm_max_a2 > 0.00122182
                                            if std_beta23 < 0.255789:
                                                return 0.206735
                                            else: #threshold std_beta23 > 0.255789
                                                return 0.215529
                                    else: #threshold norm_max_a2 > 0.000243611
                                        if norm_std_window10_a2 < 0.000357071:
                                            if norm_max_a2 < 0.000926695:
                                                if norm_a3_slope < 3.20444e-11:
                                                    if min_ecross2 < 0.162677:
                                                        return 0.159542
                                                    else: #threshold min_ecross2 > 0.162677
                                                        return 0.00115419
                                                else: #threshold norm_a3_slope > 3.20444e-11
                                                    if norm_a1_slope < 5.54021e-11:
                                                        if max_ecross3 < 0.302971:
                                                            return 0.0671952
                                                        else: #threshold max_ecross3 > 0.302971
                                                            return -0.105671
                                                    else: #threshold norm_a1_slope > 5.54021e-11
                                                        if std_ecross1 < 0.025452:
                                                            if norm_a3_slope < -2.5252e-12:
                                                                return -0.229492
                                                            else: #threshold norm_a3_slope > -2.5252e-12
                                                                if std_ecross2 < 0.021605:
                                                                    return -0.00647941
                                                                else: #threshold std_ecross2 > 0.021605
                                                                    if norm_max_window10_a1 < 0.000109385:
                                                                        if norm_a3_slope < -9.9193e-10:
                                                                            if min_ecross3 < 0.0927945:
                                                                                return 0.196191
                                                                            else: #threshold min_ecross3 > 0.0927945
                                                                                return 0.105431
                                                                        else: #threshold norm_a3_slope > -9.9193e-10
                                                                            if avg_ecross2 < 0.472691:
                                                                                if avg_beta23 < 9.8373:
                                                                                    return 0.0608082
                                                                                else: #threshold avg_beta23 > 9.8373
                                                                                    if max_ecross2 < 0.0229974:
                                                                                        if avg_ecross2 < 0.0626774:
                                                                                            return 0.188567
                                                                                        else: #threshold avg_ecross2 > 0.0626774
                                                                                            return -0.136714
                                                                                    else: #threshold max_ecross2 > 0.0229974
                                                                                        if avg_iH1 < 0.330142:
                                                                                            return -0.0270369
                                                                                        else: #threshold avg_iH1 > 0.330142
                                                                                            if min_ecross2 < 0.195824:
                                                                                                if avg_ecross1 < 0.00751233:
                                                                                                    if max_ecross1 < 0.424121:
                                                                                                        if avg_ecross1 < 0.19456:
                                                                                                            return 0.182267
                                                                                                        else: #threshold avg_ecross1 > 0.19456
                                                                                                            return -0.0158283
                                                                                                    else: #threshold max_ecross1 > 0.424121
                                                                                                        return -0.0506372
                                                                                                else: #threshold avg_ecross1 > 0.00751233
                                                                                                    if norm_std_window10_a3 < 1.90451e-05:
                                                                                                        return -0.0506544
                                                                                                    else: #threshold norm_std_window10_a3 > 1.90451e-05
                                                                                                        if max_ecross1 < 0.189913:
                                                                                                            if max_ecross1 < 0.805342:
                                                                                                                if avg_ecross2 < 0.32702:
                                                                                                                    return 0.111933
                                                                                                                else: #threshold avg_ecross2 > 0.32702
                                                                                                                    if max_ecross1 < 0.437236:
                                                                                                                        if norm_max_window10_a3 < 0.000503626:
                                                                                                                            return -0.26032
                                                                                                                        else: #threshold norm_max_window10_a3 > 0.000503626
                                                                                                                            return -0.0357359
                                                                                                                    else: #threshold max_ecross1 > 0.437236
                                                                                                                        return -0.245295
                                                                                                            else: #threshold max_ecross1 > 0.805342
                                                                                                                return 0.211091
                                                                                                        else: #threshold max_ecross1 > 0.189913
                                                                                                            if max_ecross2 < 0.178422:
                                                                                                                if max_ecross2 < 0.062879:
                                                                                                                    return -0.0732256
                                                                                                                else: #threshold max_ecross2 > 0.062879
                                                                                                                    if avg_beta23 < 10.6055:
                                                                                                                        if avg_iH1 < 0.655688:
                                                                                                                            return 0.222889
                                                                                                                        else: #threshold avg_iH1 > 0.655688
                                                                                                                            if min_ecross2 < 0.133816:
                                                                                                                                if min_beta23 < 20.7844:
                                                                                                                                    return 0.0746696
                                                                                                                                else: #threshold min_beta23 > 20.7844
                                                                                                                                    return -0.10339
                                                                                                                            else: #threshold min_ecross2 > 0.133816
                                                                                                                                return 0.0557656
                                                                                                                    else: #threshold avg_beta23 > 10.6055
                                                                                                                        return 0.210054
                                                                                                            else: #threshold max_ecross2 > 0.178422
                                                                                                                return 0.217398
                                                                                            else: #threshold min_ecross2 > 0.195824
                                                                                                return 0.100258
                                                                            else: #threshold avg_ecross2 > 0.472691
                                                                                return -0.0293922
                                                                    else: #threshold norm_max_window10_a1 > 0.000109385
                                                                        return 0.151046
                                                        else: #threshold std_ecross1 > 0.025452
                                                            return 0.046759
                                            else: #threshold norm_max_a2 > 0.000926695
                                                if avg_beta12 < 25.5357:
                                                    return 0.103998
                                                else: #threshold avg_beta12 > 25.5357
                                                    if norm_max_a3 < 4.02045e-05:
                                                        if avg_beta12 < 9.51165:
                                                            return -0.187279
                                                        else: #threshold avg_beta12 > 9.51165
                                                            return -0.288695
                                                    else: #threshold norm_max_a3 > 4.02045e-05
                                                        return 0.296791
                                        else: #threshold norm_std_window10_a2 > 0.000357071
                                            if norm_std_a1 < 9.72485e-05:
                                                if avg_beta23 < 6.25636:
                                                    if max_ecross1 < 0.0199081:
                                                        return 0.0851349
                                                    else: #threshold max_ecross1 > 0.0199081
                                                        return 0.156943
                                                else: #threshold avg_beta23 > 6.25636
                                                    if avg_ecross1 < 0.386273:
                                                        return -0.0652196
                                                    else: #threshold avg_ecross1 > 0.386273
                                                        if avg_ecross2 < 0.098411:
                                                            return 0.226988
                                                        else: #threshold avg_ecross2 > 0.098411
                                                            return 0.124236
                                            else: #threshold norm_std_a1 > 9.72485e-05
                                                if std_ecross2 < 0.00306702:
                                                    if norm_max_a3 < 7.61944e-05:
                                                        return -0.0882921
                                                    else: #threshold norm_max_a3 > 7.61944e-05
                                                        if max_ecross1 < 0.520008:
                                                            if avg_iH2 < 2.38112:
                                                                return 0.200435
                                                            else: #threshold avg_iH2 > 2.38112
                                                                return 0.223655
                                                        else: #threshold max_ecross1 > 0.520008
                                                            return -0.142755
                                                else: #threshold std_ecross2 > 0.00306702
                                                    return 0.103041
    else: #threshold max_ecross2 > 0.490431
        if max_ecross1 < 0.183113:
            return -0.0201539
        else: #threshold max_ecross1 > 0.183113
            if max_ecross2 < 0.0739176:
                return -0.116938
            else: #threshold max_ecross2 > 0.0739176
                if std_ecross2 < 0.0408983:
                    return 0.187557
                else: #threshold std_ecross2 > 0.0408983
                    return 0.208326
    #New booster
    if norm_max_a2 < 0.00355906:
        if std_beta12 < 0.0239555:
            if avg_ecross3 < 0.581285:
                if min_ecross2 < 0.188316:
                    if min_ecross2 < 0.440933:
                        if norm_max_a1 < 5.98357e-05:
                            if max_beta23 < 7.82554:
                                if norm_std_a3 < 0.000209119:
                                    if norm_a3_slope < 1.77814e-11:
                                        if min_ecross2 < 0.0157009:
                                            return 0.101414
                                        else: #threshold min_ecross2 > 0.0157009
                                            if min_ecross3 < 0.0759119:
                                                return 0.0826939
                                            else: #threshold min_ecross3 > 0.0759119
                                                return -0.175064
                                    else: #threshold norm_a3_slope > 1.77814e-11
                                        if norm_max_window10_a1 < 4.98884e-05:
                                            if max_ecross1 < 0.12984:
                                                return 0.10306
                                            else: #threshold max_ecross1 > 0.12984
                                                return 0.00582501
                                        else: #threshold norm_max_window10_a1 > 4.98884e-05
                                            if std_ecross2 < 0.00720316:
                                                if min_ecross2 < 0.073808:
                                                    if norm_a2_slope < -2.6961e-11:
                                                        if norm_a2_slope < 1.44779e-10:
                                                            return 0.179048
                                                        else: #threshold norm_a2_slope > 1.44779e-10
                                                            return 0.00042866
                                                    else: #threshold norm_a2_slope > -2.6961e-11
                                                        if std_ecross2 < 0.00387736:
                                                            if min_ecross2 < 0.448848:
                                                                if norm_max_a2 < 0.000505498:
                                                                    if norm_std_window10_a2 < 3.71475e-05:
                                                                        if std_ecross3 < 0.00167601:
                                                                            return 0.0994892
                                                                        else: #threshold std_ecross3 > 0.00167601
                                                                            return 0.0842264
                                                                    else: #threshold norm_std_window10_a2 > 3.71475e-05
                                                                        return 0.199455
                                                                else: #threshold norm_max_a2 > 0.000505498
                                                                    if norm_a3_slope < 3.68413e-11:
                                                                        return 0.123321
                                                                    else: #threshold norm_a3_slope > 3.68413e-11
                                                                        return 0.0313252
                                                            else: #threshold min_ecross2 > 0.448848
                                                                if norm_std_a2 < 0.000221735:
                                                                    if min_ecross2 < 0.171843:
                                                                        if max_ecross1 < 0.0174665:
                                                                            if avg_ecross1 < 0.0252647:
                                                                                if norm_max_a3 < 0.000432776:
                                                                                    if min_ecross3 < 0.282843:
                                                                                        return 0.0234215
                                                                                    else: #threshold min_ecross3 > 0.282843
                                                                                        if norm_std_a2 < 5.18277e-05:
                                                                                            return -0.172843
                                                                                        else: #threshold norm_std_a2 > 5.18277e-05
                                                                                            return -0.0937441
                                                                                else: #threshold norm_max_a3 > 0.000432776
                                                                                    if norm_a3_slope < -2.38606e-10:
                                                                                        if norm_std_a2 < 5.78475e-05:
                                                                                            return 0.020185
                                                                                        else: #threshold norm_std_a2 > 5.78475e-05
                                                                                            if std_ecross3 < 0.00226187:
                                                                                                if std_ecross1 < 0.0322609:
                                                                                                    return 0.138161
                                                                                                else: #threshold std_ecross1 > 0.0322609
                                                                                                    return 0.208705
                                                                                            else: #threshold std_ecross3 > 0.00226187
                                                                                                return -0.234611
                                                                                    else: #threshold norm_a3_slope > -2.38606e-10
                                                                                        return 0.193611
                                                                            else: #threshold avg_ecross1 > 0.0252647
                                                                                if norm_max_a2 < 0.000283862:
                                                                                    if norm_a3_slope < 4.14368e-12:
                                                                                        return -0.263957
                                                                                    else: #threshold norm_a3_slope > 4.14368e-12
                                                                                        return -0.177881
                                                                                else: #threshold norm_max_a2 > 0.000283862
                                                                                    return 0.20097
                                                                        else: #threshold max_ecross1 > 0.0174665
                                                                            if avg_ecross3 < 0.213137:
                                                                                return -0.262738
                                                                            else: #threshold avg_ecross3 > 0.213137
                                                                                return -0.142179
                                                                    else: #threshold min_ecross2 > 0.171843
                                                                        if norm_max_window10_a3 < 9.80231e-05:
                                                                            return 0.192955
                                                                        else: #threshold norm_max_window10_a3 > 9.80231e-05
                                                                            return 0.0128549
                                                                else: #threshold norm_std_a2 > 0.000221735
                                                                    if norm_a3_slope < -2.03043e-10:
                                                                        return 0.000893683
                                                                    else: #threshold norm_a3_slope > -2.03043e-10
                                                                        return 0.167714
                                                        else: #threshold std_ecross2 > 0.00387736
                                                            return 0.196704
                                                else: #threshold min_ecross2 > 0.073808
                                                    return 0.0557619
                                            else: #threshold std_ecross2 > 0.00720316
                                                if max_ecross1 < 0.0888592:
                                                    return -0.0779141
                                                else: #threshold max_ecross1 > 0.0888592
                                                    if norm_a3_slope < 3.14964e-10:
                                                        return 0.187355
                                                    else: #threshold norm_a3_slope > 3.14964e-10
                                                        return 0.0361253
                                else: #threshold norm_std_a3 > 0.000209119
                                    if norm_max_a2 < 0.0025515:
                                        return -0.15041
                                    else: #threshold norm_max_a2 > 0.0025515
                                        if norm_max_a2 < 7.75719e-05:
                                            return -0.108677
                                        else: #threshold norm_max_a2 > 7.75719e-05
                                            return -0.0561483
                            else: #threshold max_beta23 > 7.82554
                                if norm_std_a1 < 7.96117e-06:
                                    if norm_std_window10_a1 < 0.000259881:
                                        return -0.25891
                                    else: #threshold norm_std_window10_a1 > 0.000259881
                                        return 0.201996
                                else: #threshold norm_std_a1 > 7.96117e-06
                                    return -0.275021
                        else: #threshold norm_max_a1 > 5.98357e-05
                            if norm_std_a2 < 3.61786e-05:
                                return -0.0135145
                            else: #threshold norm_std_a2 > 3.61786e-05
                                if max_ecross1 < 0.168917:
                                    if avg_ecross1 < 0.188442:
                                        if max_ecross1 < 0.00463208:
                                            return 0.0971399
                                        else: #threshold max_ecross1 > 0.00463208
                                            if norm_a2_slope < -2.83421e-12:
                                                return 0.0465092
                                            else: #threshold norm_a2_slope > -2.83421e-12
                                                return -0.0476736
                                    else: #threshold avg_ecross1 > 0.188442
                                        return -0.0168042
                                else: #threshold max_ecross1 > 0.168917
                                    return 0.128459
                    else: #threshold min_ecross2 > 0.440933
                        return -0.0213192
                else: #threshold min_ecross2 > 0.188316
                    return 0.18202
            else: #threshold avg_ecross3 > 0.581285
                if std_beta12 < 0.00810568:
                    if avg_beta12 < 24.6458:
                        return -0.0510898
                    else: #threshold avg_beta12 > 24.6458
                        if std_ecross1 < 0.00523089:
                            if min_ecross3 < 0.0237425:
                                return 0.0686479
                            else: #threshold min_ecross3 > 0.0237425
                                return 0.205728
                        else: #threshold std_ecross1 > 0.00523089
                            return 0.129045
                else: #threshold std_beta12 > 0.00810568
                    if avg_ecross3 < 0.177969:
                        if max_beta12 < 19.1951:
                            return 0.112435
                        else: #threshold max_beta12 > 19.1951
                            return 0.234229
                    else: #threshold avg_ecross3 > 0.177969
                        if avg_ecross2 < 0.551656:
                            return 0.0193774
                        else: #threshold avg_ecross2 > 0.551656
                            if norm_max_window10_a1 < 0.00125592:
                                return 0.202983
                            else: #threshold norm_max_window10_a1 > 0.00125592
                                if min_ecross3 < 0.397917:
                                    return -0.264678
                                else: #threshold min_ecross3 > 0.397917
                                    if norm_a3_slope < 9.47349e-11:
                                        if max_ecross1 < 0.0601853:
                                            if norm_max_a2 < 0.00020299:
                                                if max_ecross1 < 0.0405993:
                                                    return 0.0992423
                                                else: #threshold max_ecross1 > 0.0405993
                                                    if norm_max_a1 < 0.00255332:
                                                        return -0.0867887
                                                    else: #threshold norm_max_a1 > 0.00255332
                                                        if std_beta12 < 0.261757:
                                                            if norm_a3_slope < 6.84633e-10:
                                                                return 0.213005
                                                            else: #threshold norm_a3_slope > 6.84633e-10
                                                                return 0.13892
                                                        else: #threshold std_beta12 > 0.261757
                                                            if min_ecross3 < 0.731175:
                                                                return 0.0779848
                                                            else: #threshold min_ecross3 > 0.731175
                                                                return -0.178257
                                            else: #threshold norm_max_a2 > 0.00020299
                                                return 0.129637
                                        else: #threshold max_ecross1 > 0.0601853
                                            if norm_max_a1 < 0.00614871:
                                                return 0.169838
                                            else: #threshold norm_max_a1 > 0.00614871
                                                return -0.208149
                                    else: #threshold norm_a3_slope > 9.47349e-11
                                        if std_ecross3 < 0.0498309:
                                            return -0.169085
                                        else: #threshold std_ecross3 > 0.0498309
                                            if max_ecross1 < 0.556466:
                                                if norm_a2_slope < -1.70331e-10:
                                                    return -0.0619181
                                                else: #threshold norm_a2_slope > -1.70331e-10
                                                    return 0.0630709
                                            else: #threshold max_ecross1 > 0.556466
                                                if max_ecross1 < 0.376607:
                                                    if norm_std_a2 < 2.98833e-05:
                                                        return 0.0312646
                                                    else: #threshold norm_std_a2 > 2.98833e-05
                                                        return 0.145869
                                                else: #threshold max_ecross1 > 0.376607
                                                    if norm_std_a3 < 2.58237e-05:
                                                        return 0.0397131
                                                    else: #threshold norm_std_a3 > 2.58237e-05
                                                        if norm_max_a3 < 8.03388e-05:
                                                            return 0.0642967
                                                        else: #threshold norm_max_a3 > 8.03388e-05
                                                            if norm_std_window10_a2 < 2.39979e-05:
                                                                return 0.108897
                                                            else: #threshold norm_std_window10_a2 > 2.39979e-05
                                                                if norm_a3_slope < -5.2726e-11:
                                                                    return 0.201529
                                                                else: #threshold norm_a3_slope > -5.2726e-11
                                                                    if norm_max_a2 < 6.29804e-05:
                                                                        return 0.0159037
                                                                    else: #threshold norm_max_a2 > 6.29804e-05
                                                                        if max_ecross1 < 0.388119:
                                                                            if min_ecross2 < 0.321093:
                                                                                if norm_a3_slope < -1.61623e-11:
                                                                                    if min_ecross1 < 0.18798:
                                                                                        if max_ecross1 < 0.0360264:
                                                                                            if avg_ecross2 < 0.0967646:
                                                                                                if avg_ecross2 < 0.855924:
                                                                                                    return 0.210407
                                                                                                else: #threshold avg_ecross2 > 0.855924
                                                                                                    return 0.120718
                                                                                            else: #threshold avg_ecross2 > 0.0967646
                                                                                                if norm_std_a1 < 0.000130138:
                                                                                                    return -0.336337
                                                                                                else: #threshold norm_std_a1 > 0.000130138
                                                                                                    if std_ecross3 < 0.00424902:
                                                                                                        return -0.0706484
                                                                                                    else: #threshold std_ecross3 > 0.00424902
                                                                                                        if avg_ecross3 < 0.860312:
                                                                                                            return 0.109871
                                                                                                        else: #threshold avg_ecross3 > 0.860312
                                                                                                            return 0.202151
                                                                                        else: #threshold max_ecross1 > 0.0360264
                                                                                            if min_beta23 < 6.58327:
                                                                                                if avg_iH2 < 1.12666:
                                                                                                    return 0.0937395
                                                                                                else: #threshold avg_iH2 > 1.12666
                                                                                                    return -0.107997
                                                                                            else: #threshold min_beta23 > 6.58327
                                                                                                if std_beta12 < 0.0204262:
                                                                                                    return -0.127211
                                                                                                else: #threshold std_beta12 > 0.0204262
                                                                                                    if avg_ecross3 < 0.426273:
                                                                                                        return 0.20303
                                                                                                    else: #threshold avg_ecross3 > 0.426273
                                                                                                        return 0.10674
                                                                                    else: #threshold min_ecross1 > 0.18798
                                                                                        if norm_max_a2 < 0.00213262:
                                                                                            return 0.181735
                                                                                        else: #threshold norm_max_a2 > 0.00213262
                                                                                            if min_ecross3 < 0.0955355:
                                                                                                return 0.0576261
                                                                                            else: #threshold min_ecross3 > 0.0955355
                                                                                                if avg_beta12 < 22.0593:
                                                                                                    return 0.21183
                                                                                                else: #threshold avg_beta12 > 22.0593
                                                                                                    return 0.173599
                                                                                else: #threshold norm_a3_slope > -1.61623e-11
                                                                                    if norm_max_window10_a3 < 0.000544767:
                                                                                        if min_ecross3 < 0.0198739:
                                                                                            return 0.212398
                                                                                        else: #threshold min_ecross3 > 0.0198739
                                                                                            return 0.144711
                                                                                    else: #threshold norm_max_window10_a3 > 0.000544767
                                                                                        if avg_ecross2 < 0.0773143:
                                                                                            if min_ecross1 < 0.377155:
                                                                                                return 0.0263316
                                                                                            else: #threshold min_ecross1 > 0.377155
                                                                                                if min_beta23 < 17.0672:
                                                                                                    if norm_std_window10_a1 < 0.000551241:
                                                                                                        if std_ecross3 < 0.102685:
                                                                                                            if avg_ecross3 < 0.412503:
                                                                                                                if min_ecross3 < 0.149467:
                                                                                                                    if min_ecross1 < 0.00177278:
                                                                                                                        if norm_std_window10_a2 < 0.000150529:
                                                                                                                            return -0.166376
                                                                                                                        else: #threshold norm_std_window10_a2 > 0.000150529
                                                                                                                            return -0.268313
                                                                                                                    else: #threshold min_ecross1 > 0.00177278
                                                                                                                        return -0.104803
                                                                                                                else: #threshold min_ecross3 > 0.149467
                                                                                                                    return 0.203814
                                                                                                            else: #threshold avg_ecross3 > 0.412503
                                                                                                                if min_ecross2 < 0.312793:
                                                                                                                    return 0.122772
                                                                                                                else: #threshold min_ecross2 > 0.312793
                                                                                                                    return -0.109466
                                                                                                        else: #threshold std_ecross3 > 0.102685
                                                                                                            if max_ecross1 < 0.96281:
                                                                                                                return 0.101324
                                                                                                            else: #threshold max_ecross1 > 0.96281
                                                                                                                return 0.0428742
                                                                                                    else: #threshold norm_std_window10_a1 > 0.000551241
                                                                                                        if max_ecross1 < 0.312326:
                                                                                                            return 0.198039
                                                                                                        else: #threshold max_ecross1 > 0.312326
                                                                                                            return 0.117067
                                                                                                else: #threshold min_beta23 > 17.0672
                                                                                                    if std_beta12 < 0.0399052:
                                                                                                        if max_ecross1 < 0.400007:
                                                                                                            return 0.0927008
                                                                                                        else: #threshold max_ecross1 > 0.400007
                                                                                                            return -0.138746
                                                                                                    else: #threshold std_beta12 > 0.0399052
                                                                                                        return 0.219448
                                                                                        else: #threshold avg_ecross2 > 0.0773143
                                                                                            if std_ecross1 < 0.000203684:
                                                                                                if norm_max_a1 < 0.00152371:
                                                                                                    if min_ecross1 < 0.00046447:
                                                                                                        return 0.153826
                                                                                                    else: #threshold min_ecross1 > 0.00046447
                                                                                                        return 0.113487
                                                                                                else: #threshold norm_max_a1 > 0.00152371
                                                                                                    return 0.126772
                                                                                            else: #threshold std_ecross1 > 0.000203684
                                                                                                return -0.323581
                                                                            else: #threshold min_ecross2 > 0.321093
                                                                                return -0.0292401
                                                                        else: #threshold max_ecross1 > 0.388119
                                                                            if norm_max_a3 < 3.99891e-05:
                                                                                if std_ecross2 < 0.0222053:
                                                                                    return 0.055821
                                                                                else: #threshold std_ecross2 > 0.0222053
                                                                                    if norm_max_a1 < 3.95527e-05:
                                                                                        if norm_std_window10_a2 < 5.14637e-05:
                                                                                            if avg_ecross1 < 0.287079:
                                                                                                return -0.014057
                                                                                            else: #threshold avg_ecross1 > 0.287079
                                                                                                return -0.231503
                                                                                        else: #threshold norm_std_window10_a2 > 5.14637e-05
                                                                                            return 0.187695
                                                                                    else: #threshold norm_max_a1 > 3.95527e-05
                                                                                        return 0.0711863
                                                                            else: #threshold norm_max_a3 > 3.99891e-05
                                                                                if norm_a3_slope < 4.47311e-12:
                                                                                    if norm_a2_slope < 1.33464e-11:
                                                                                        return -0.191112
                                                                                    else: #threshold norm_a2_slope > 1.33464e-11
                                                                                        return -0.301368
                                                                                else: #threshold norm_a3_slope > 4.47311e-12
                                                                                    return 0.219213
        else: #threshold std_beta12 > 0.0239555
            if std_ecross3 < 0.0398594:
                return 0.121982
            else: #threshold std_ecross3 > 0.0398594
                return 0.121765
    else: #threshold norm_max_a2 > 0.00355906
        if std_beta12 < 0.00876266:
            if max_ecross1 < 0.108274:
                if std_beta12 < 0.013895:
                    if norm_max_a3 < 0.00128479:
                        if std_ecross3 < 0.00282083:
                            if norm_max_a3 < 0.000115432:
                                if norm_max_a3 < 0.000158993:
                                    return -0.06276
                                else: #threshold norm_max_a3 > 0.000158993
                                    return 0.14283
                            else: #threshold norm_max_a3 > 0.000115432
                                return 0.0945088
                        else: #threshold std_ecross3 > 0.00282083
                            return 0.214348
                    else: #threshold norm_max_a3 > 0.00128479
                        return -0.0437017
                else: #threshold std_beta12 > 0.013895
                    if norm_a3_slope < -2.57141e-11:
                        return 0.0123148
                    else: #threshold norm_a3_slope > -2.57141e-11
                        return -0.229114
            else: #threshold max_ecross1 > 0.108274
                if norm_max_window10_a1 < 7.9273e-06:
                    return -0.173226
                else: #threshold norm_max_window10_a1 > 7.9273e-06
                    return 0.203401
        else: #threshold std_beta12 > 0.00876266
            if min_ecross2 < 0.385864:
                if norm_std_window10_a2 < 0.000127659:
                    return 0.205693
                else: #threshold norm_std_window10_a2 > 0.000127659
                    return 0.0589371
            else: #threshold min_ecross2 > 0.385864
                return -0.0235388