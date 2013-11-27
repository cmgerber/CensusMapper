CREATE TYPE usertype as ENUM ('super', 'regular');
CREATE TYPE geolevel as ENUM ('default', 'state', 'county', 'tract');
CREATE TYPE disptype as ENUM ('solid choropleth', 'hash choropleth', 'dot density', 'bubble');

CREATE TABLE Users (
    UserID serial4 PRIMARY KEY,
    UserName varchar(20),
    EmailAddress varchar(50),
    Password char(32),
    AccessLevel usertype
);

CREATE TABLE Maps (
    MapID serial8 PRIMARY KEY,
    MapName varchar(50),
    UserID int4 REFERENCES Users (UserID) ON DELETE CASCADE,
    CenterLatitude float8,
    CenterLongitude float8,
    ZoomLevel int2
);

CREATE TABLE DataLayers (
    DataLayersID serial8 PRIMARY KEY,
    MapID int8 REFERENCES Maps (MapID) ON DELETE CASCADE,
    MeasureID int4 REFERENCES Measures (MeasureID),
    Year int4,
    DisplayOrder int2,
    DisplayGeography geolevel,
    DisplayType disptype,
    Visible boolean,
    ColorSchemeName varchar(8),
    NumCategories int2,
    Transparency float4
);

CREATE TABLE ValueBreaks (
    ValueBreaksID serial8 PRIMARY KEY,
    DataLayersID int8 REFERENCES DataLayers (DataLayersID) ON DELETE CASCADE,
    CategoryNumber int2,
    MinValue float4,
    MaxValue float4
);

CREATE TABLE ColorSchemes (
    ColorID serial4 PRIMARY KEY,
    ColorSchemeName varchar(8),
    NumCategories int2,
    CriticalValue float4,
    CategoryNumber int2,
    RedValue int2,
    GreenValue int2,
    BlueValue int2,
    SchemeType varchar(11)
);

CREATE TABLE Categories (
    CategoryID serial4 PRIMARY KEY,
    Category varchar(20),
    DefaultColorScheme varchar(8)
);

CREATE TABLE Measures (
    MeasureID serial4 PRIMARY KEY,
    CategoryID int4 REFERENCES Categories (CategoryID),
    Description varchar(100),
    DefaultBreaks varchar(100)
);

CREATE TABLE Numerator (
    NumeratorID serial4 PRIMARY KEY,
    MeasureID int4 REFERENCES Measures (MeasureID),
    FieldID char(9)
);

CREATE TABLE Denominator (
    DenominatorID serial4 PRIMARY KEY,
    MeasureID int4 REFERENCES Measures (MeasureID),
    FieldID char(9)
);

/*
-- Run this to clear database:
DROP TABLE Users CASCADE;
DROP TABLE Maps CASCADE;
DROP TABLE DataLayers CASCADE;
DROP TABLE ValueBreaks;
DROP TABLE ColorSchemes;
DROP TABLE Measures;
DROP TABLE Numerator;
DROP TABLE Denominator;
DROP TYPE usertype;
DROP TYPE geolevel;
DROP TYPE disptype;
*/
