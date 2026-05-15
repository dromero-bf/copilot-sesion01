import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './welcome.html',
  styleUrl: './welcome.scss',
})
export class WelcomeComponent implements OnInit {
  username = '';
  currentTime = new Date();

  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.loadUserInfo();
    setInterval(() => {
      this.currentTime = new Date();
    }, 1000);
  }

  loadUserInfo(): void {
    const token = this.authService.getToken();
    if (!token) return;

    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    this.http.get<{ username: string }>('http://localhost:8000/users/me', { headers }).subscribe({
      next: (user) => {
        this.username = user.username;
      },
      error: () => {
        this.username = 'Usuario';
      },
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
