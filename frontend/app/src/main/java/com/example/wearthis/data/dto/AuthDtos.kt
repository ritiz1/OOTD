package com.example.wearthis.data.dto

import com.google.gson.annotations.SerializedName

data class LoginRequestDto(
    val email: String,
    val password: String
)

data class RegisterRequestDto(
    val email: String,
    val password: String,
    @SerializedName("password_confirm")
    val passwordConfirm: String,
    @SerializedName("first_name")
    val firstName: String = "",
    @SerializedName("last_name")
    val lastName: String = ""
)

data class RefreshTokenRequestDto(
    val refresh: String
)

data class RefreshTokenResponseDto(
    val access: String
)

data class UserDto(
    val id: String,
    val email: String,
    @SerializedName("first_name")
    val firstName: String,
    @SerializedName("last_name")
    val lastName: String,
    @SerializedName("date_joined")
    val dateJoined: String
)

data class AuthResponseDto(
    val access: String,
    val refresh: String,
    val user: UserDto
)

data class UpdateUserRequestDto(
    @SerializedName("first_name")
    val firstName: String,
    @SerializedName("last_name")
    val lastName: String
)
