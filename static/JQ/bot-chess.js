function game() {
    const xAxis = ["A", "B", "C", "D", "E", "F", "G", "H"]
    const yAxis = [1, 2, 3, 4, 5, 6, 7, 8]
    //Checkerboard coordinates
    let action = {
        "from": null,
        "to": "auto",
        "currentPlayer": null,
        "winner": null,
        "botOwn": "black",
        "saveRecord": false
    }
    //Initial game Setup
    $(".grid").click(function () {
        //Binding click events
        if (checkWinner())
            return
        //Check the winner
        let $grid = $(this)
        if ($grid.children(".chess").length == 1) {
            clearBeforeMove()
            $grid.toggleClass("active")
            //choose a piece
        }
        if (!action.from && !action.currentPlayer && $grid.children(".chess").length == 1) {
            let $child = $($grid.children(".chess")[0])
            if ($child.attr("color") == "white") {
                action.from = $grid
                action.currentPlayer = $child.attr("color")
                // console.log($child.attr("color"))
                // console.log($grid)
            }
            return
            //Get the initial pieces and positions color
        } else if ($grid.children(".chess").length == 1) {
            let $child = $($grid.children(".chess")[0])
            console.log($child.attr("color"))
            if (action.currentPlayer == $child.attr("color")) {
                action.from = $grid
                return
                //Get subsequent pieces
                //Determine if you are choosing a white piece
            } else {
                clearBeforeMove()
                //cancel move
                //Can't choose a black piece
            }
        }
        if (!action.from) {
            return
        }

        if (action.currentPlayer == "white") {
            playChess($grid)
            botChess()
            //player move
            //bot move
        }
    })
    //Chess main function
    function playChess($grid) {
        let $fromChild = $(action.from.children(".chess")[0])
        let moveGrids = moveScope($fromChild)
        let attackGrids = attackScope($fromChild)
        let gridId = $grid ? $grid.attr("id") : null//step record

        if (moveGrids.length == 0 && attackGrids.length == 0) {
            return
            //Not move
        } else {
            if ((!action.currentPlayer && action.to == "auto") || (action.currentPlayer == action.botOwn && action.to == "auto")) {
                gridId = attackGrids.length > 0 ? attackGrids[0] : moveGrids[0]
                $grid = $("#" + gridId)
                //Move
            }
        }
        if (gridId != action[2] && (moveGrids.indexOf(gridId) != -1 || attackGrids.indexOf(gridId) != -1)) {
            let $fromGrid = action.from
            let $toGrid = $grid
            clearBeforeMove()
            $fromGrid.remove($fromChild)
            $toGrid.empty()
            $toGrid.append($fromChild)
            if ($fromChild.hasClass("initial")) {
                $fromChild.removeClass("initial")
            }
            if ($fromChild.hasClass("pawn") && (getPosition($toGrid)[1] == 1 || getPosition($toGrid)[1] == 8)) {
                $fromChild.removeClass("pawn")
                $fromChild.addClass("queen")
            }
            action.from = null
            action.currentPlayer = action.currentPlayer == "white" ? "black" : "white"
        }
        action.winner = chessWinner()
        saveRecord()
        checkWinner()
    }

    //The movement coordinates of different pieces
    function moveScope(piece) {
        let scope = []
        let position = getPosition(piece.parent())
        //Get piece initial position
        if (piece.hasClass("pawn")) {
            let operate = piece.hasClass("white") ? "+" : "-"
            let $grid = $("#" + position[0] + (calculate(position[1], 1, operate)))
            // calculate move
            if ($grid.children().length == 0) {
                scope.push($grid.attr("id"))
            }
            if ($grid.children().length == 0 && piece.hasClass("initial")) {
                let $grid = $("#" + position[0] + (calculate(position[1], 2, operate)))
                if ($grid.children().length == 0) {
                    scope.push($grid.attr("id"))
                }
            }
            return scope
        }

        if (piece.hasClass("rook")) {
            let centerGrid = piece.parent()
            console.log(centerGrid)
            let directions = [top, right, bottom, left]
            for (let direction of directions) {
                let tempGrid = direction(centerGrid)
                // console.log(tempGrid)
                while (tempGrid != undefined) {
                    if (tempGrid.children().length == 0) {
                        scope.push(tempGrid.attr("id"))
                        tempGrid = direction(tempGrid)
                    } else {
                        break
                    }
                }
            }
            return scope
        }
        //Rook Move
        if (piece.hasClass("knight")) {
            let centerGrid = piece.parent()
            let nearGrid, farGrid
            let routes = [
                [top, [topLeft, topRight]],
                [right, [topRight, bottomRight]],
                [bottom, [bottomLeft, bottomRight]],
                [left, [topLeft, bottomLeft]]
            ]

            for (let route of routes) {
                let unidirection = route[0]
                let bidirection = route[1]
                nearGrid = unidirection(centerGrid)

                if (nearGrid != undefined) {
                    for (let direction of bidirection) {
                        farGrid = direction(nearGrid)
                        if (farGrid != undefined && farGrid.children(".chess").length == 0) {
                            scope.push(farGrid.attr("id"))
                        }
                    }
                }
            }
            return scope
        }
        // Knight Move
        if (piece.hasClass("bishop")) {
            let centerGrid = piece.parent()
            let tempGrid
            let directions = [topRight, bottomRight, bottomLeft, topLeft]

            for (let direction of directions) {
                tempGrid = direction(centerGrid)
                while (tempGrid != undefined) {
                    if (tempGrid.children().length == 0) {
                        scope.push(tempGrid.attr("id"))
                        tempGrid = direction(tempGrid)
                    } else {
                        break
                    }
                }
            }
            return scope
        }
        // Bishop move
        if (piece.hasClass("queen")) {
            let centerGrid = piece.parent()
            let tempGrid
            let directions = [top, topRight, right, bottomRight, bottom, bottomLeft, left, topLeft]

            for (let direction of directions) {
                tempGrid = direction(centerGrid)
                while (tempGrid != undefined) {
                    if (tempGrid.children().length == 0) {
                        scope.push(tempGrid.attr("id"))
                        tempGrid = direction(tempGrid)
                    } else {
                        break
                    }
                }
            }
            return scope
        }
        // Queen Move
        if (piece.hasClass("king")) {
            let centerGrid = piece.parent()
            let tempGrid
            let directions = [top, topRight, right, bottomRight, bottom, bottomLeft, left, topLeft]

            for (let direction of directions) {
                tempGrid = direction(centerGrid)
                if (tempGrid != undefined && tempGrid.children(".chess").length == 0) {
                    scope.push(tempGrid.attr("id"))
                }
            }
            return scope
        }
        //King move
    }
    //Piece attack mode
    function attackScope(piece) {
        let scope = []
        if (piece.hasClass("pawn")) {
            for (let grid of attackDirection(piece)) {
                if (grid != undefined && grid.children().length == 1
                    && $(grid.children()[0]).attr("color") != piece.attr("color")) {
                    scope.push(grid.attr("id"))
                }
            }
            return scope
        }
        // Pawn attack
        if (piece.hasClass("rook")) {
            let centerGrid = piece.parent()
            let directions = [top, right, bottom, left]
            for (let direction of directions) {
                let tempGrid = direction(centerGrid)
                while (tempGrid != undefined) {
                    if (tempGrid.children().length == 1) {
                        if ($(tempGrid.children()[0]).attr("color") != piece.attr("color")) {
                            scope.push(tempGrid.attr("id"))
                        }
                        break
                    } else {
                        tempGrid = direction(tempGrid)
                    }
                }
            }
            return scope
        }
        // Rook attack
        if (piece.hasClass("knight")) {
            let centerGrid = piece.parent()
            let nearGrid, farGrid
            let routes = [
                [top, [topLeft, topRight]],
                [right, [topRight, bottomRight]],
                [bottom, [bottomLeft, bottomRight]],
                [left, [topLeft, bottomLeft]]
            ]

            for (let route of routes) {
                let unidirection = route[0]
                let bidirection = route[1]

                nearGrid = unidirection(centerGrid)
                if (nearGrid != undefined) {
                    for (let direction of bidirection) {
                        farGrid = direction(nearGrid)
                        if (farGrid != undefined && farGrid.children(".chess").length == 1 && $(farGrid.children(".chess")[0]).attr("color") != piece.attr("color")) {
                            scope.push(farGrid.attr("id"))
                        }
                    }
                }
            }
            return scope
        }
        // Knight attack
        if (piece.hasClass("bishop")) {
            let centerGrid = piece.parent()
            let tempGrid
            let directions = [topRight, bottomRight, bottomLeft, topLeft]

            for (let direction of directions) {
                tempGrid = direction(centerGrid)
                while (tempGrid != undefined) {
                    if (tempGrid.children().length == 1) {
                        if ($(tempGrid.children()[0]).attr("color") != piece.attr("color")) {
                            scope.push(tempGrid.attr("id"))
                        }
                        break
                    } else {
                        tempGrid = direction(tempGrid)
                    }
                }
            }
            return scope
        }
        // Bishop attack
        if (piece.hasClass("queen")) {
            let centerGrid = piece.parent()
            let tempGrid
            let directions = [top, topRight, right, bottomRight, bottom, bottomLeft, left, topLeft]

            for (let direction of directions) {
                tempGrid = direction(centerGrid)
                while (tempGrid != undefined) {
                    if (tempGrid.children().length == 1) {
                        if ($(tempGrid.children()[0]).attr("color") != piece.attr("color")) {
                            scope.push(tempGrid.attr("id"))
                        }
                        break
                    } else {
                        tempGrid = direction(tempGrid)
                    }
                }
            }
            return scope
        }
        //Queen attack
        if (piece.hasClass("king")) {
            let centerGrid = piece.parent()
            let tempGrid
            let directions = [top, topRight, right, bottomRight, bottom, bottomLeft, left, topLeft]

            for (let direction of directions) {
                tempGrid = direction(centerGrid)
                if (tempGrid != undefined && tempGrid.children(".chess").length == 1 && $(tempGrid.children(".chess")[0]).attr("color") != piece.attr("color")) {
                    scope.push(tempGrid.attr("id"))
                }
            }

            return scope
        }
        //King attack
    }

    // Chess Bot
    // Random move
    function botChess() {
        for (let i = 0; i < 1000; i++) {
            if (action.currentPlayer && action.currentPlayer != "black")
                return
            let randomNum = parseInt(Math.random() * 15)
            let piece = $("div[color=black]")[randomNum]
            if (piece) {
                action.from = $(piece).parent()
                playChess()
            }
        }
    }

    function chessWinner() {
        if ($(".chess.white.king").length == 0) return "black"
        else if ($(".chess.black.king").length == 0) return "white"
        else return null
    }

    function checkWinner() {
        if (action.winner) {
            $("#winner").html(`<h4><span class="badge badge-success">` + action.winner + `</span></h4>`)
            return true
        }
        return false
    }

    function saveRecord() {
        if (action.winner && !action.saveRecord) {
            let flag = action.winner == action.botOwn ? 0 : 1
            $.ajax({
                url: "/play/chess/saveRecord?flag=" + flag,
                async: false,
                success: function (data) {
                    action.saveRecord = true
                }
            })
        }
    }
    //Keep records
    chessRange()

    function chessRange() {
        setInterval(function () {
            doChessRange()
        }, 3000)
    }
    //Update leaderboards regularly
    function doChessRange() {
        let h = `<li class="list-group-item d-flex justify-content-between align-items-center">
                 <span><span class="badge badge-primary badge-pill">{{win}}</span>
                 &nbsp&nbsp&nbsp&nbsp&nbsp<span class="badge badge-primary badge-pill">{{lose}}</span></span>{{username}}</li>`
        $.ajax({
            url: "/play/chess/range",
            success: function (data) {
                $("#winDashboard").html("")
                for (let i = 0; i < data.length; i++) {
                    let d = data[i]
                    $("#winDashboard").append(h.replace("{{username}}", d.username)
                        .replace("{{win}}", d.chessWin).replace("{{lose}}", d.chessLose))
                }
            }
        })
    }
    //Update ranking list
    function clearBeforeMove() {
        $(".grid").removeClass("active")
    }
    //Uncheck
    function calculate(param1, param2, operation) {
        if (operation == "+")
            return param1 + param2
        if (operation == "-")
            return param1 - param2
    }
    //Calculate the coordinates
    function attackDirection(piece) {
        if (piece.hasClass("pawn")) {
            let centerGrid = piece.parent()
            let scope = piece.hasClass("white") ? [topLeft(centerGrid), topRight(centerGrid)]
                : [bottomLeft(centerGrid), bottomRight(centerGrid)]
            return scope
        }
    }
    //Pawn walk straight and eat sideways
    function getPosition(grid) {
        let gridId = $(grid).attr("id")
        let x = gridId[0]
        let y = parseInt(gridId[1])

        return [x, y]
    }
    //Get the position of the piece

    function isMarginTop(grid) {
        let position = getPosition(grid)
        return position[1] == yAxis[7]
    }
    //Reach the top

    function isMarginBottom(grid) {
        let position = getPosition(grid)
        return position[1] == yAxis[0]
    }
    //Reach the bottom
    function isMarginLeft(grid) {
        let position = getPosition(grid)
        return position[0] == xAxis[0]
    }
    //Reach left
    function isMarginRight(grid) {
        let position = getPosition(grid)
        return position[0] == xAxis[7]
    }
    //Reach Right
    function top(grid) {
        let position = getPosition(grid)
        if (isMarginTop(grid) == true) {
            return undefined
        } else {
            return $("#" + position[0] + (position[1] + 1))
        }
    }
    // Move Up
    function bottom(grid) {
        let position = getPosition(grid)
        if (isMarginBottom(grid) == true) {
            return undefined
        } else {
            return $("#" + position[0] + (position[1] - 1))
        }
    }
    // Move Down
    function left(grid) {
        let position = getPosition(grid)
        if (isMarginLeft(grid) == true) {
            return undefined
        } else {
            return $("#" + xAxis[xAxis.indexOf(position[0]) - 1] + position[1])
        }
    }
    //Move left
    function right(grid) {
        let position = getPosition(grid)
        if (isMarginRight(grid) == true) {
            return undefined
        } else {
            return $("#" + xAxis[xAxis.indexOf(position[0]) + 1] + position[1])
        }
    }
    //Move left
    function topLeft(grid) {
        let position = getPosition(grid)
        if (isMarginTop(grid) || isMarginLeft(grid)) {
            return undefined
        } else {
            return $("#" + xAxis[xAxis.indexOf(position[0]) - 1] + (position[1] + 1))
        }
    }
    //Move up left
    function topRight(grid) {
        let position = getPosition(grid)
        if (isMarginTop(grid) || isMarginRight(grid)) {
            return undefined
        } else {
            return $("#" + xAxis[xAxis.indexOf(position[0]) + 1] + (position[1] + 1))
        }
    }
    //Move up right
    function bottomLeft(grid) {
        let position = getPosition(grid)
        if (isMarginBottom(grid) || isMarginLeft(grid)) {
            return undefined
        } else {
            return $("#" + xAxis[xAxis.indexOf(position[0]) - 1] + (position[1] - 1))
        }
    }
    //Move down left
    function bottomRight(grid) {
        let position = getPosition(grid)
        if (isMarginBottom(grid) || isMarginRight(grid)) {
            return undefined
        } else {
            return $("#" + xAxis[xAxis.indexOf(position[0]) + 1] + (position[1] - 1))
        }
    }
    //Move down right
}

game()
