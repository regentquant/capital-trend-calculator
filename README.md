# capital-trend-calculator

Updated Tuesday, December 26, 2023 (PST)

Version 2.0

Simpler and easier to use.

Written with love by Curry Yao

Curry Yao, CEO and Engineer at Regentquant.com




    --- Sacle Up ---
    entry_list = '''QQQ@401@CALL@2023-12-27@2023-12-26
    QQQ@402@CALL@2023-12-27@2023-12-26
    QQQ@403@CALL@2023-12-27@2023-12-26
    QQQ@404@CALL@2023-12-27@2023-12-26
    QQQ@405@CALL@2023-12-27@2023-12-26
    QQQ@406@CALL@2023-12-27@2023-12-26
    QQQ@407@CALL@2023-12-27@2023-12-26
    QQQ@408@CALL@2023-12-27@2023-12-26
    QQQ@409@CALL@2023-12-27@2023-12-26
    QQQ@410@CALL@2023-12-27@2023-12-26
    QQQ@411@CALL@2023-12-27@2023-12-26
    QQQ@412@CALL@2023-12-27@2023-12-26
    QQQ@413@CALL@2023-12-27@2023-12-26
    QQQ@414@CALL@2023-12-27@2023-12-26
    QQQ@415@CALL@2023-12-27@2023-12-26
    QQQ@416@CALL@2023-12-27@2023-12-26
    QQQ@417@CALL@2023-12-27@2023-12-26
    QQQ@418@CALL@2023-12-27@2023-12-26
    QQQ@419@CALL@2023-12-27@2023-12-26
    QQQ@420@CALL@2023-12-27@2023-12-26
    QQQ@421@CALL@2023-12-27@2023-12-26'''.split('\n')
    
    for entry in entry_list:
    
        download_intraday_data_and_save_to_a_txt_file(entry)
        calculate_capital_trend(entry)
