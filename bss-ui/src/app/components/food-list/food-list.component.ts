import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'food-list',
  templateUrl: './food-list.component.html',
  styleUrls: ['./food-list.component.css']
})
export class FoodListComponent implements OnInit {

  foods: Food[] = [];

	constructor(private route: ActivatedRoute, private userService: AppService) { }

	ngOnInit() {
		this.getFoods();
	}

	getFoods(): void {
		this.userService.getFoods().subscribe(food => this.foods = food);
	}
  

}
