CREATE TABLE session (sessionId int not null auto_increment, 
					  name varchar(20), 
					  constraint pk_sessionId primary key (sessionId));

CREATE TABLE role (roleId int not null auto_increment,
				   name varchar(20),
				   constraint pk_roleId primary key (roleId));

CREATE TABLE user (userId int not null auto_increment, 
				   name varchar(20), sessionId int not null,
				   roleId int not null, 
				   constraint pk_userId primary key (userId),
				   constraint fk_sessionId foreign key (sessionId) references session (sessionId),
				   constraint fk_roleId foreign key (roleId) references role (roleId));

CREATE TABLE story (storyId int not null auto_increment, 
					name varchar(50), description varchar(100),
					storyPoints int, sessionId int not null,
					constraint pk_storyId primary key (storyId),
					constraint fk_session_Id foreign key (sessionId) references session (sessionId));

