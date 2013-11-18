INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('censusmapper', 'censusmapper@ischool.berkeley.edu', md5('censusmapper'), 'super');
INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('sandra', 'sandra@ischool.berkeley.edu', md5('sandra'), 'regular');
INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('colin', 'colin.gerber@ischool.berkeley.edu', md5('colin'), 'regular');
INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('jason', 'jost@ischool.berkeley.edu', md5('jason'), 'regular');

INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('censusmapper', 'censusmapper@ischool.berkeley.edu', 'censusmapper', 'super');
INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('sandra', 'sandra@ischool.berkeley.edu', 'sandra', 'regular');
INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('colin', 'colin.gerber@ischool.berkeley.edu', 'colin', 'regular');
INSERT INTO Users (UserName, EmailAddress, Password, AccessLevel) VALUES ('jason', 'jost@ischool.berkeley.edu', 'jason', 'regular');

INSERT INTO Maps (MapName, UserID, CenterLatitude, CenterLongitude, ZoomLevel) VALUES ('% Asian', 2, 0, 0, 11);

INSERT INTO DataLayers (MapID, MeasureID, Year, DisplayOrder, DisplayGeography, DisplayType, Visible, ColorSchemeName, NumCategories, Transparency) VALUES (1, 0, 0, 0, 'state', 'solid choropleth', True, 'PuBu', 7, 1);

INSERT INTO ValueBreaks (DataLayersID, CategoryNumber, MinValue, MaxValue) VALUES (1, 1, 0, 10);
INSERT INTO ValueBreaks (DataLayersID, CategoryNumber, MinValue, MaxValue) VALUES (1, 2, 10, 20);
INSERT INTO ValueBreaks (DataLayersID, CategoryNumber, MinValue, MaxValue) VALUES (1, 3, 20, 30);
