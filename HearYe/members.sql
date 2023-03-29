CREATE TABLE [dbo].[members]
(
  [Id] INT NOT NULL PRIMARY KEY,
  name varchar(50) NOT NULL,
  discord_username varchar(50) NOT NULL,
  discord_id varchar(50) NOT NULL,
  discord_guild_id varchar(50) NOT NULL,
  fanfare_title varchar(50) NULL
)
