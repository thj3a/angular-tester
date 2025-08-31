import { Component, Input, Output, EventEmitter } from '@angular/core';
import { User } from '../models/user.interface';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-user-card',
  template: `
    <div class="user-card" *ngIf="user">
      <h2>{{ user.name }}</h2>
      <p>{{ user.email }}</p>
      <button (click)="onEdit()">Edit</button>
      <button (click)="onDelete()">Delete</button>
    </div>
  `,
  styles: [`
    .user-card {
      border: 1px solid #ccc;
      padding: 16px;
      border-radius: 8px;
      max-width: 300px;
    }
    
    h2 {
      color: #333;
      margin-top: 0;
    }
    
    button {
      background-color: #007bff;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      margin-right: 8px;
    }
    
    button:last-child {
      background-color: #dc3545;
    }
  `]
})
export class UserCardComponent {
  @Input() user: User | null = null;
  @Output() edit = new EventEmitter<User>();
  @Output() delete = new EventEmitter<User>();

  constructor(private userService: UserService) {}

  onEdit(): void {
    if (this.user) {
      this.edit.emit(this.user);
    }
  }

  onDelete(): void {
    if (this.user) {
      this.delete.emit(this.user);
    }
  }
}