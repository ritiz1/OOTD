package com.example.wearthis.data.remote

import com.example.wearthis.data.dto.AuthResponseDto
import com.example.wearthis.data.dto.ClothingUploadResponseDto
import com.example.wearthis.data.dto.LoginRequestDto
import com.example.wearthis.data.dto.RecommendRequestDto
import com.example.wearthis.data.dto.RecommendationResponseDto
import com.example.wearthis.data.dto.RefreshTokenRequestDto
import com.example.wearthis.data.dto.RefreshTokenResponseDto
import com.example.wearthis.data.dto.RegisterRequestDto
import com.example.wearthis.data.dto.UpdateUserRequestDto
import com.example.wearthis.data.dto.UserDto
import okhttp3.MultipartBody
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Part

interface ApiService {
    @GET("api/wardrobe/items/")
    suspend fun clothing(): List<com.example.wearthis.data.dto.RemoteClothingDto>

    @retrofit2.http.DELETE("api/wardrobe/items/{id}/")
    suspend fun deleteClothing(@retrofit2.http.Path("id") id: String)

    @POST("api/auth/register/")
    suspend fun register(@Body request: RegisterRequestDto): AuthResponseDto

    @POST("api/auth/token/")
    suspend fun login(@Body request: LoginRequestDto): AuthResponseDto

    @POST("api/auth/token/refresh/")
    suspend fun refreshToken(
        @Body request: RefreshTokenRequestDto
    ): RefreshTokenResponseDto

    @GET("api/auth/me/")
    suspend fun getCurrentUser(): UserDto

    @PATCH("api/auth/me/")
    suspend fun updateCurrentUser(@Body request: UpdateUserRequestDto): UserDto

    @Multipart
    @POST("api/wardrobe/describe/")
    suspend fun describeClothing(
        @Part image: MultipartBody.Part
    ): ClothingUploadResponseDto

    @POST("api/wardrobe/recommend/")
    suspend fun recommend(
        @Body request: RecommendRequestDto
    ): RecommendationResponseDto
}
