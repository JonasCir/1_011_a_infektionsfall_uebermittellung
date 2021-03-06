package de.coronavirus.imis.api.dto;


import de.coronavirus.imis.config.domain.UserRole;
import lombok.Data;

@Data
public class RegisterUserRequest {
	private String username;
	private String password;
	private String firstName;
	private String lastName;
	private UserRole userRole;
}
