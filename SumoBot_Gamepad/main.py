TESTING = False

if TESTING:
    import tx_test
    tx_test.main()
else:
    import gamepad_qt
    gamepad_qt.main()


